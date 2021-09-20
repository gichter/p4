from tinydb import TinyDB, where

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

        """ call this function to save actual tournament state, even in between rounds.
            use load_state to retrieve the data saved.
        """
def save_state(tournament):
    pass

    """ loads the saved tournament 
        cases : - 0-7 players are in the tournament => finishes to get the players 
                - rounds have started :
    """


def load_state(tournament):
    pass


def search_players_by_lastname(lastname):
    print(db_players.search(where('lastname') == lastname))
    input("")


def clear_saves():
    db_players.truncate()
    db_tournament.truncate()
