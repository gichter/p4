#! /usr/bin/env python3
# coding: utf-8

import view
import model


# Demande à l'utilisateur de saisir les informations d'un joueur afin de l'ajouter à la base de données.
def add_player(prompted_player):
    player = model.Player(
        lastname=prompted_player['lastname'],
        firstname=prompted_player['firstname'],
        birthdate=prompted_player['birthdate'],
        sex=prompted_player['sex']
        )
    return player.insert_user()


# Demande à l'utilisateur de saisir les informations d'un tournoi
def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    tournament = model.Tournament(
        name=prompted_tournament['name'],
        location=prompted_tournament['location'],
        time_control=prompted_tournament['time_control'],
        description=prompted_tournament['description'],
        date_start=prompted_tournament['date_start'],
        date_end=prompted_tournament['date_end'],
        number_of_turns=prompted_tournament['number_of_turns'],
    )
    return tournament


# Permet de créer un tournoi et d'y ajouter des joueurs
def create_tournament():
    tournament = add_tournament()
    tournament = create_player_pool(tournament, 8)
    return tournament.insert_tournament()


# Ajoute à un objet tournoi un nombre donné de joueurs.
# On peut ajouter un joueur existant ou un nouveau joueur.
def create_player_pool(tournament, number_of_players_to_add):
    for i in range(9 - number_of_players_to_add, 9):
        view.clear_terminal()
        choice = input(
            'Ajout du joueur numéro ' + str(i) + '.\n'
            '1: Créer un nouveau Joueur\n'
            '2: Rechercher Joueur\n'
            '0 : Quitter et enregistrer le tournoi\n')
        while True:
            if(choice == '1'):
                view.clear_terminal()
                player_id = add_player(view.prompt_new_player())
                tournament.add_player(player_id)
                print('Player ' + str(i) + 'added')
                break
            elif(choice == '2'):  # search player then add him to the tournament
                lastname = input('Nom du joueur ?')
                player_id = view.select_player(model.search_players_by_lastname(lastname))
                tournament.add_player(player_id)
                break
            elif(choice == '0'):
                return tournament
    return tournament


# Permet à l'utilisateur de modifier un joueur après selection de ce dernier
def edit_player():
    lastname = input('Saisissez le nom du joueur à modifier')
    player_id = view.select_player(model.search_players_by_lastname(lastname))
    model.update_player(view.prompt_new_player(), player_id)
    input("Joueur modifié avec succès. Appuyez sur une touche pour continuer")


# Permet à l'utilisateur de modifier un tournoi après selection de ce dernier
def edit_tournament():
    name = input('Saisissez le nom du tournoi à modifier')
    tournament_id = view.select_tournament(model.search_tournament_by_name(name)).doc_id
    model.update_tournament_dict(view.prompt_new_tournament(), tournament_id)
    input("Tournoi modifié avec succès. Appuyez sur une touche pour continuer")


# Renvoie un objet tournoi après avoir demandé à l'utilisateur de selectionner un tournoi dans une liste
def import_tournament():
    name = input('Saisissez le nom du tournoi que vous souhaitez charger :\n')
    tournament = view.select_tournament(model.search_tournament_by_name(name))
    if(len(tournament.players) < 8):
        tournament = create_player_pool(tournament, 8 - len(tournament.players))
    tournament.update_tournament(tournament.doc_id)
    return tournament


# Fonction de tri de la liste des joueurs d'un tournoi donné.
# Trie les joueurs dans l'ordre décroissant de leur score de tournoi, puis trie les égalités selon le score total.
# Fait appel à 'players_played_together()' afin de ne pas refaire jouer deux joueurs ensemble plusieurs fois.
def create_player_list(tournament):
    player_list = []
    for player_id in tournament.players:
        p_dict = model.search_player_by_doc_id(player_id)
        p = model.Player(
            lastname=p_dict['lastname'], firstname=p_dict['firstname'], birthdate=p_dict['birthdate'],
            sex=p_dict['sex'], total_score=p_dict['total_score'])
        p.update_doc_id(player_id)
        player_list.append(p)
    if (len(tournament.rounds) == 0):
        player_list.sort(key=lambda x: x.total_score, reverse=True)
        l1 = player_list[0:4]
        l2 = player_list[4:8]
        player_list = []
        for i in range(4):
            player_list.append(l1[i])
            player_list.append(l2[i])
    else:
        for p in player_list:
            for r in tournament.rounds:
                for i in range(4):
                    if(r[i+3][0][0] == p.doc_id):
                        p.score += float(r[i+3][0][1])
                    if(r[i+3][1][0] == p.doc_id):
                        p.score += float(r[i+3][1][1])
        player_list.sort(key=lambda x: (-x.score, -x.total_score))
        if (len(tournament.rounds) >= 2):
            p = []
            for i in range(3):
                k = 1
                while True:
                    if not (players_played_together(tournament, (player_list[0]), player_list[k])):
                        p.append(player_list[0])
                        p.append(player_list[k])
                        player_list.pop(0)
                        player_list.pop(k - 1)
                        break
                    if(k+1 == len(player_list)):
                        break
                    k += 1
            player_list = p + player_list
    return player_list


# Vérifie si deux joueurs ont déjà joué ensemble dans un tournoi donné.
# Le tuple (joueur1, joueur2) est passé dans toutes les étapes de tous les rounds existants d'un tournoi.
def players_played_together(tournament, player1, player2):
    for r in tournament.rounds:
        for i in range(4):
            if((r[i+3][0][0] == player1.doc_id) and (r[i+3][1][0] == player2.doc_id)
                    or (r[i+3][0][0] == player2.doc_id) and (r[i+3][1][0] == player1.doc_id)):
                return True
    return False


# Prend en entrée un tournoi.
# Tant que toues les rondes ne sont pas jouées, relance une ronde et l'inscrit en base de données.
# La fonction vérifie que le tournoi n'est pas fini.
def play_tournament(tournament):
    while len(tournament.rounds) < int(tournament.number_of_turns):
        player_list = create_player_list(tournament)
        print(player_list)
        input()
        tournament.rounds.append(tournament.create_round(player_list))
        tournament.update_tournament(tournament.doc_id)
    if int(tournament.number_of_turns) == len(tournament.rounds):
        view.clear_terminal()
        print('Tournoi terminé. Pour afficher les résultats de ce dernier, rendez-vous dans la liste des tournois. \
        \nAppuyez sur entrée pour retourner au menu principal')
        input()


# Boucle principale du programme. Connectée à la vue "main_menu"
def main():
    while True:
        view.main_menu()
        choice = input("Choix de l'option :")
        if choice == "1":
            add_player(view.prompt_new_player())
        elif choice == "2":
            create_tournament()
        elif choice == "3":
            t = import_tournament()
        elif choice == "4":
            view.display_players(model.load_players())
        elif choice == "5":
            view.display_tournaments(model.load_tournaments())
        elif choice == "6":
            edit_player()
        elif choice == "7":
            edit_tournament()
        elif choice == "8":
            try:
                play_tournament(t)
            except t.DoesNotExist:
                print("Veuillez charger un tournoi avec l'option numéro 3.")
        elif choice == "0":
            break
        else:
            print("Veuillez saisir une option disponible")


if __name__ == "__main__":
    main()
