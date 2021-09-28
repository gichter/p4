from tinydb import TinyDB, Query, table
import re

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
    __slots__ = ['name', 'location', 'date', 'players', 'number_of_turns', 'instances', 'time_control', 'description']

    def __init__(self, data):
        self.players = []
        for key in data:
            setattr(self, key, data[key])

    def add_player(self, player):
        self.players.append(player)

    def insert_tournament(self):
        serialized_tournament = {
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'number_of_turns': self.number_of_turns,
            'instances': self.instances,
            'players': self.players,
            'time_control': self.time_control,
            'description': self.description,
        }
        return db_tournament.insert(serialized_tournament)


def update_player(player, player_id):
    db_players.upsert(table.Document({
            'lastname': player['lastname'],
            'firstname': player['firstname'],
            'birthdate': player['birthdate'],
            'sex': player['sex'],
            }, doc_id=int(player_id)))


def update_tournament(tournament, tournament_id):
    if (isinstance(tournament_id, str)):
        tournament_id = int(tournament_id)
    db_tournament.upsert(table.Document({
            'name': tournament.name,
            'location': tournament.location,
            'date': tournament.date,
            'number_of_turns': tournament.number_of_turns,
            'instances': tournament.instances,
            'players': tournament.players,
            'time_control': tournament.time_control,
            'description': tournament.description,
        }, doc_id=tournament_id))


def update_tournament_dict(tournament, tournament_id):
    db_tournament.upsert(table.Document({
            'name': tournament['name'],
            'location': tournament['location'],
            'date': tournament['date'],
            'number_of_turns': tournament['number_of_turns'],
            'instances': tournament['instances'],
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


def create_tournament_from_dict(dict):
    input(Tournament(table.Document(dict)))


def clear_saves():
    db_players.truncate()
    db_tournament.truncate()
