from tinydb import TinyDB, Query

db = TinyDB('players.json')

class Player(object):
    name = ''

    def __init__(self, name):
        self.name = name