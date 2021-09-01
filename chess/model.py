from tinydb import TinyDB, Query

db = TinyDB('players.json')

class Player(object):
    def __init__(self, lastname, firstname, birthdate, sex, elo):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo


    def insert_user(self):
        serialized_player = {
            'lastname': self.lastname,
            'firstname': self.firstname,
            'birthdate': self.birthdate,
            'sex': self.sex,
            'elo': self.elo,
        }
        return db.insert(serialized_player)

class Tournament(object):
    def __init__(self, name, location, date, number_of_turns, 
                    instances, players, time_control, description):
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = number_of_turns
        self.instances = instances
        self.players = players
        self.time_control = time_control
        self.description = description
    
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
        return db.insert(serialized_tournament)
