from tinydb import TinyDB, Query, table
import re
from datetime import datetime
import view

db_players = TinyDB('players.json')
db_tournament = TinyDB('tournament.json')


class Player(object):
    def __init__(self, lastname, firstname, birthdate, sex, total_score=0):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.sex = sex
        self.score = 0
        self.total_score = total_score
        self.doc_id = 0

    def insert_user(self):
        serialized_player = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birthdate': self.birthdate,
            'sex': self.sex,
            'score': self.score,
            'total_score': self.total_score
        }
        return db_players.insert(serialized_player)

    def update_user(self):
        pass

    def update_doc_id(self, doc_id):
        self.doc_id = doc_id


class Tournament(object):
    def __init__(
        self, name, location, time_control,
            description, date_start=0, date_end=0, number_of_turns=4, players=[], rounds=[]):
        self.name = name
        self.location = location
        self.time_control = time_control
        self.description = description
        self.number_of_turns = number_of_turns
        self.players = players
        self.date_start = date_start
        self.date_end = date_end
        self.rounds = rounds
        self.doc_id = 0

    # Associe l'id d'un tournoi à sa représentatiojn objet
    def update_doc_id(self, doc_id):
        self.doc_id = doc_id

    def add_player(self, player):
        self.players.append(player)

    # Créé un round selon la liste de joueurs ordonnée
    def create_round(self, players_list):
        round = ["Round " + str(len(self.rounds) + 1), str(datetime.now())]
        view.print_round(players_list, len(self.rounds)+1)
        for i in range(4):
            round.append(view.ask_match_result(players_list[i*2], players_list[i*2+1]))
        round.insert(2, str(datetime.now()))
        return round

    def insert_tournament(self):
        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'number_of_turns': self.number_of_turns,
            'rounds': self.rounds,
            'players': self.players,
            'time_control': self.time_control,
            'description': self.description,
        }
        return db_tournament.insert(serialized_tournament)

    def update_tournament(self, tournament_id):
        if (isinstance(tournament_id, str)):
            tournament_id = int(tournament_id)
        db_tournament.upsert(table.Document({
                'name': self.name,
                'location': self.location,
                'date_start': self.date_start,
                'date_end': self.date_end,
                'number_of_turns': self.number_of_turns,
                'rounds': self.rounds,
                'players': self.players,
                'time_control': self.time_control,
                'description': self.description,
            }, doc_id=tournament_id))

    # Affichage d'un round joué
    def print_round(self, round_number):
        player_ids = []
        player_scores = []
        for i in range(4):
            player_ids.append(self.rounds[round_number][i+3][0][0])
            player_ids.append(self.rounds[round_number][i+3][1][0])
            player_scores.append(self.rounds[round_number][i+3][0][1])
            player_scores.append(self.rounds[round_number][i+3][1][1])
        print(self.rounds[round_number][0])
        print(datetime.fromisoformat(self.rounds[round_number][1]).strftime("Début de la ronde : %d/%m/%Y à %H:%M"))
        print(datetime.fromisoformat(self.rounds[round_number][2]).strftime("Fin de la ronde : %d/%m/%Y à %H:%M"))
        print('\nRésultats de la ronde :\n----------------------------------------------------')
        j = 1
        for i in range(0, 8, 2):
            print(
                'Match n°' + str(j) + ' : ' + get_player_name_with_id(player_ids[i]) + ' (' +
                player_scores[i] + ') vs ' +
                get_player_name_with_id(player_ids[i+1]) + ' (' + player_scores[i+1] + ')' + '\n' +
                '----------------------------------------------------')
            j += 1

# Affichage des résultats d'un tournoi
    def print_results(self):
        player_list = []
        for player_id in self.players:
            p_dict = search_player_by_doc_id(player_id)
            p = Player(
                lastname=p_dict['lastname'], firstname=p_dict['firstname'], birthdate=p_dict['birthdate'],
                sex=p_dict['sex'], total_score=p_dict['total_score'])
            p.update_doc_id(player_id)
            player_list.append(p)
        for p in player_list:
            i = 0
            for r in self.rounds:
                for i in range(4):
                    if(r[i+3][0][0] == p.doc_id):
                        p.score += float(r[i+3][0][1])
                    if(r[i+3][1][0] == p.doc_id):
                        p.score += float(r[i+3][1][1])
        player_list.sort(key=lambda x: (-x.score, -x.total_score))
        i = 0
        print('Classement du tournoi :')
        for p in player_list:
            i += 1
            print(str(i) + ': ' + p.firstname + ' ' + p.lastname + ' : ' + str(p.score) + ' / ' + str(p.total_score))


def get_player_name_with_id(player_id):
    player = search_player_by_doc_id(player_id)
    return player['firstname'] + ' ' + player['lastname']


def update_player(player, player_id):
    db_players.upsert(table.Document({
            'lastname': player['lastname'],
            'firstname': player['firstname'],
            'birthdate': player['birthdate'],
            'sex': player['sex'],
            }, doc_id=int(player_id)))


def update_tournament_dict(tournament, tournament_id):
    db_tournament.upsert(table.Document({
            'name': tournament['name'],
            'location': tournament['location'],
            'date': tournament['date'],
            'number_of_turns': tournament['number_of_turns'],
            'rounds': tournament['rounds'],
            'time_control': tournament['time_control'],
            'description': tournament['description'],
        }, doc_id=int(tournament_id)))


def load_players():
    return db_players.all()


def load_tournaments():
    return db_tournament.all()


def search_players_by_lastname(lastname):
    Players = Query()
    return db_players.search(Players.lastname.matches(lastname, flags=re.IGNORECASE))


def search_player_by_doc_id(doc_id):
    return db_players.get(doc_id=doc_id)


def search_tournament_by_name(name):
    Tournaments = Query()
    return db_tournament.search(Tournaments.name.matches(name, flags=re.IGNORECASE))


def clear_saves():
    db_players.truncate()
    db_tournament.truncate()
