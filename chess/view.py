from os import system, name

from model import Tournament

"""
    Menu principal
    """
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
    print("6: Modifier les informations d'un joueur")
    print("7: Modifier les informations d'un tournoi")
    print("8: Lancer le dernier tournoi chargé (Choix numéro 3)")
    print("0: Quitter")
    print("_________________________________________________________")
    print("")


    """
    Affichage de la liste des joueurs
    """
def show_player_list(player_db):
    print("Il y a " + str(len(player_db)) + " joueurs inscrits en base de données")
    for item in player_db:
        print(item.doc_id)
        print(item['lastname'] + " " + item['firstname'] + ", " + str(item['score']) + " elo")


    """
    Menu de création de tournoi
    """
def prompt_new_tournament():
    clear_terminal()
    name = input("Nom du tournoi ?\n")
    location = input("Lieu ?\n")
    time_control = input("Format ?\n")
    description = input("Description ?\n")
    date_start = input("Date de début ?\n")
    date_end = input("Date de fin ?\n")
    number_of_turns = input("Nombre de tours ?\n")
    tournament = {
        'name': name,
        'location': location,
        'time_control': time_control,
        'description': description,
        'date_start': date_start,
        'date_end': date_end,
        'number_of_turns': number_of_turns,
    }
    return tournament


    """
    Menu de création de joueur
    """
def prompt_new_player():
    clear_terminal()
    print("Veuillez entrer le joueur")
    lastname = input("nom ? ")
    firstname = input("prénom ? ")
    birthdate = input("date de naissance ? ")
    sex = input("sexe ? ")
    player = {
        'lastname': lastname,
        'firstname': firstname,
        'birthdate': birthdate,
        'sex': sex,
    }
    return player


    """
    Menu d'affichage de la liste des joueurs
    """
def display_players(players):
    clear_terminal()
    print(
        'Sélectionner l\'affichage des joueurs désiré :\n'
        '1: Par ordre alphabétique\n'
        '2: Par classement\n'
        '0: Quitter et revenir au menu principal\n'
        )
    while True:
        choice = input('')
        if choice == '1':
            players.sort(key=lambda x: x['lastname'])
            break
        elif choice == '2':
            players.sort(key=lambda x: -x['total_score'])
            break
        elif choice == '0':
            return 0
    i = 0
    clear_terminal()
    for player in players:
        i += 1
        print(str(i) + ": " + player["lastname"] + " " + player["firstname"] + " (" + str(player["total_score"]) + ")")
    input("Appuyez sur une touche pour continuer")


    """
    Menu d'affichage de la liste des tournois
    """
def display_tournaments(tournaments):
    clear_terminal()
    i = 0
    for tournament in tournaments:
        i += 1
        print(str(i) + ": " + tournament["name"] + " - " + tournament["date_start"])
    choice = int(input('\nSélectionnez l\'id du tournoi à visualiser\nSaisir 0 pour retourner au menu principal\n'))
    if choice > 0 and choice <= i:
        tournament = Tournament(tournaments[choice-1]["name"],
        tournaments[choice-1]["location"],
        tournaments[choice-1]["time_control"],
        tournaments[choice-1]["description"],
        tournaments[choice-1]["date_start"],
        tournaments[choice-1]["date_end"],
        tournaments[choice-1]["number_of_turns"],
        tournaments[choice-1]["players"],
        tournaments[choice-1]["rounds"]
        )
        while True:
            clear_terminal()
            print(tournament.name + ' (' + tournament.date_start + '): ' + tournament.location)
            if (len(tournament.rounds) == int(tournament.number_of_turns)):
                print('Tournoi terminé. Afficher les résultats en tapant 9')
            j = 0
            if(len(tournament.rounds) > 0):
                for r in tournament.rounds:
                    j += 1
                    print(str(j) + ': ' + r[0])
                choice = int(input(
                    '\nSélectionnez l\'id de la tournée à visualiser\nSaisir 0 pour retourner au menu principal\n'))
                if choice == 0:
                    break
                if choice == 9 and len(tournament.rounds) == int(tournament.number_of_turns):
                    clear_terminal()
                    tournament.print_results()
                else:
                    print(tournament.print_round(choice-1))
            input("Appuyez sur une touche pour continuer")
            if tournament.rounds == []:
                break
    elif choice == 0:
        return 0


def display_tournaments_list(tournaments):
    i = 0
    for tournament in tournaments:
        i += 1
        print(str(i) + ": " + tournament["name"] + " - " + tournament["date_start"])
    choice = int(input('\nSélectionnez l\'id du tournoi à charger\nSaisir 0 pour retourner au menu principal\n'))
    if choice > 0 and choice <= i:
        tournament = Tournament(tournaments[choice-1]["name"],
        tournaments[choice-1]["location"],
        tournaments[choice-1]["time_control"],
        tournaments[choice-1]["description"],
        tournaments[choice-1]["date_start"],
        tournaments[choice-1]["date_end"],
        tournaments[choice-1]["number_of_turns"],
        tournaments[choice-1]["players"],
        tournaments[choice-1]["rounds"]
        )
    tournament.update_doc_id(tournaments[choice-1].doc_id)
    return tournament


    """
    Selection du joueur à modifier
    """
def select_player(players):
    display_players(players)
    choice = input("Quel joueur souhaitez-vous modifier ? Sélectionnez son index.")
    return list(players)[int(choice) - 1].doc_id


    """
    Selection du tournoi à modifier
    """
def select_tournament(tournaments): 
    tournament = display_tournaments_list(tournaments)
    input("Tournoi " + tournament.name + " selectionné avec succès. Appuyez sur une touche pour continuer.\n")
    return tournament


    """
    Fonction d'affichage d'une ronde
    """
def print_round(players_list, round_number):
    clear_terminal()
    players_names = []
    for p in players_list:
        players_names.append(
            str(p.doc_id) + ': ' + p.firstname + ' ' + p.lastname +
            ' (' + str(p.total_score) + ')/(' + str(p.score) + ')')

    print(
        '\nRound numéro ' + str(round_number) + '\n' +
        '----------------------------------------------------\n'
        'Match n°1 : ' + players_names[0] + ' vs ' + players_names[1] + '\n' +
        '----------------------------------------------------\n'
        'Match n°2 : ' + players_names[2] + ' vs ' + players_names[3] + '\n' +
        '----------------------------------------------------\n'
        'Match n°3 : ' + players_names[4] + ' vs ' + players_names[5] + '\n' +
        '----------------------------------------------------\n'
        'Match n°4 : ' + players_names[6] + ' vs ' + players_names[7] + '\n' +
        '----------------------------------------------------\n' +
        'Appuyez sur entrée pour saisir les résultats'
    )
    input()


    """
    Fonction de demande de résultat d'un match d'une ronde donnée
    Renvoie le tuple de résultat ([j1, résultat], [j2, résultat])
    """
def ask_match_result(player1, player2):
    clear_terminal()
    print(
        'Sélectionnez le joueur qui a gagné le match, ou 0 pour saisir une égalité :\n' +
        '1: ' + player1.firstname + ' ' + player1.lastname + '\n'
        '2: ' + player2.firstname + ' ' + player2.lastname + '\n'
    )
    choice = input()
    match = []
    if choice == '1':
        match = ([player1.doc_id, '1'], [player2.doc_id, '0'])
    elif choice == '2':
        match = ([player1.doc_id, '0'], [player2.doc_id, '1'])
    elif choice == '0':
        match = ([player1.doc_id, '0.5'], [player2.doc_id, '0.5'])
    return match


    """
    Fonction de nettoyage de l'affichage de la console
    """
def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
