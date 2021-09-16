from tinydb import TinyDB

db_players = TinyDB('players.json')
db_tournament = TinyDB('tournament.json')


class Player(object):
    def __init__(self, lastname, firstname, birthdate, sex):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.sex = sex
        self.ranking = 0

    def insert_player(self):
        serialized_player = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birthdate': self.birthdate,
            'sex': self.sex,
            'ranking': self.ranking,
        }
        return db_players.insert(serialized_player)


class Tournament(object):
    def __init__(self, name, location, date, number_of_turns, instances, time_control, description):
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = number_of_turns
        self.instances = instances
        self.players = []
        self.time_control = time_control
        self.description = description

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

