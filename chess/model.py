from tinydb import TinyDB, Query, table
import re

db_players = TinyDB('players.json')
db_tournament = TinyDB('tournament.json')


class Player(object):
    def __init__(self, lastname, firstname, birthdate, sex):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.sex = sex
        self.score = 0
        self.total_score = 0

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


def load_players():
    return db_players.all()


def search_players_by_lastname(lastname):
    Players = Query()
    return db_players.search(Players.lastname.matches(lastname, flags=re.IGNORECASE))


def search_tournament_by_name(name):
    Tournaments = Query()
    return db_tournament.search(Tournaments.name.matches(name, flags=re.IGNORECASE))


def create_tournament_from_dict(dict):
    input(Tournament(table.Document(dict)))


def clear_saves():
    db_players.truncate()
    db_tournament.truncate()
