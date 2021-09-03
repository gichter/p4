def main_menu():
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
