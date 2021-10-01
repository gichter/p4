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
    def __init__(self, name, location, date_start, date_end, time_control, description, number_of_turns=4, players=[], rounds=[]):
        self.name = name
        self.location = location
        self.date_start = date_start
        self.date_end = date_end
        self.time_control = time_control
        self.description = description
        self.number_of_turns = number_of_turns
        self.players = players
        self.rounds = rounds
        self.doc_id = 0

    def __init__(self, data):
        self.players = []
        for key in data:
            setattr(self, key, data[key])

    def update_doc_id(self, doc_id):
        self.doc_id = doc_id

    def add_player(self, player):
        self.players.append(player)

    #takes the ordered player list to use to create the matches
    def create_round(self, players_list):
        round = ["Round" + str(len(self.rounds) + 1), str(datetime.now())]
        view.print_round(players_list, len(self.rounds)+1)
        for i in range(4):
            round.append(view.ask_match_result(players_list[i*2], players_list[i*2+1]))
        round.insert(2, str(datetime.now()))
        return round
    

    def insert_tournament(self):
        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'date': self.date,
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
                'date': self.date,
                'number_of_turns': self.number_of_turns,
                'rounds': self.rounds,
                'players': self.players,
                'time_control': self.time_control,
                'description': self.description,
            }, doc_id=tournament_id))


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
