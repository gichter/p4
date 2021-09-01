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