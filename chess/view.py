from os import system, name
from pprint import pprint

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
    print("0: Quitter")
    print("_________________________________________________________")
    print("")

def show_player_list(player_db):
    print("Il y a " + str(len(player_db)) + " joueurs inscrits en base de données")
    for item in player_db:
        print(item['name'] + ", " + str(item['elo']) + " elo")
    return 0

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

def prompt_new_player(player_number):
    clear_terminal()
    print("Veuillez entrer le joueur numéro ", player_number)
    lastname = input("nom ?")
    firstname = input("prénom ?")
    birthdate = input("date de naissance ?")
    sex = input("sexe ?")
    elo = input("elo ?")
    player = {
        'lastname': lastname,
        'firstname': firstname,
        'birthdate': birthdate,
        'sex': sex,
        'elo': elo,
    }
    return player

def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

#debug function (pprint tounament) TODO : delete this
def print_object(obj):
    pprint(obj.__dict__)
    for player in obj.players:
        pprint(player.__dict__)
    input()