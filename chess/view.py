from os import system, name
from pprint import pprint
from tinydb import where


def main_menu():
    clear_terminal()
    print("_________________________________________________________")
    print("")
    print("Menu principal")
    print("1: Ajouter un joueur")
    print("2: Créer un tournoi")
    print("3: Charger un tournoi")
    print("4: Liste des joueurs enregistrés")
    print("5: Liste des tournois")
    print("6: Récupérer le dernier tournoi en cours")
    print("0: Quitter")
    print("_________________________________________________________")
    print("")


def show_player_list(player_db):
    print("Il y a " + str(len(player_db)) + " joueurs inscrits en base de données")
    for item in player_db:
        print(item.doc_id)
        print(item['lastname'] + " " + item['firstname'] + ", " + str(item['score']) + " elo")


def prompt_new_tournament():
    clear_terminal()
    name = input("nom du tournoi ?")
    location = input("Lieu ?")
    date = input("Date ?")
    number_of_turns = input("Nombre de tours ?")
    instances = input("Tournées ?")
    time_control = input("Format ?")
    description = input("Description ?")
    tournament = {
        'name': name,
        'location': location,
        'date': date,
        'number_of_turns': number_of_turns,
        'instances': instances,
        'time_control': time_control,
        'description': description,
    }
    return tournament


def prompt_new_player():
    clear_terminal()
    print("Veuillez entrer le joueur")
    lastname = input("nom ?")
    firstname = input("prénom ?")
    birthdate = input("date de naissance ?")
    sex = input("sexe ?")
    player = {
        'lastname': lastname,
        'firstname': firstname,
        'birthdate': birthdate,
        'sex': sex,
    }
    return player


def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# debug function (pprint tounament) TODO : delete this
def print_object(obj):
    pprint(obj.__dict__)
    for player in obj.players:
        pprint(player.__dict__)
    input()
