#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB
import model
from faker import Faker


def show_players():
    db = TinyDB("players.json")
    view.show_player_list(db)


def add_player(prompted_player):
    """
    fake = Faker('fr_FR')
    for i in range(50):
        player = model.Player(
        lastname=fake.last_name(),
        firstname=fake.first_name(),
        birthdate=fake.date_of_birth().isoformat(),
        sex='M',
        total_score=fake.pyint(0, 2500, 10)
        )
        player.insert_user()
    """
    player = model.Player(
        lastname=prompted_player['lastname'],
        firstname=prompted_player['firstname'],
        birthdate=prompted_player['birthdate'],
        sex=prompted_player['sex']
        )
    return player.insert_user()


def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    tournament = model.Tournament({
        "name": prompted_tournament['name'],
        "location": prompted_tournament['location'],
        "date": prompted_tournament['date'],
        "number_of_turns": prompted_tournament['number_of_turns'],
        "instances": prompted_tournament['instances'],
        "time_control": prompted_tournament['time_control'],
        "description": prompted_tournament['description']
    })
    return tournament


def create_tournament():
    tournament = add_tournament()
    tournament = create_player_pool(tournament, 8)
    return tournament.insert_tournament()


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


def edit_player():
    lastname = input('Saisissez le nom du joueur à modifier')
    player_id = view.select_player(model.search_players_by_lastname(lastname))
    model.update_player(view.prompt_new_player(), player_id)
    input("Joueur modifié avec succès. Appuyez sur une touche pour continuer")


def edit_tournament():
    name = input('Saisissez le nom du tournoi à modifier')
    tournament_id = view.select_tournament(model.search_tournament_by_name(name)).doc_id
    model.update_tournament_dict(view.prompt_new_tournament(), tournament_id)
    input("Tournoi modifié avec succès. Appuyez sur une touche pour continuer")


# returns a tournament object after asking the user to select one
def import_tournament():
    name = input('Saisissez le nom du tournoi que vous souhaitez charger :\n')
    tournament_data = view.select_tournament(model.search_tournament_by_name(name))
    tournament = model.Tournament(tournament_data)
    tournament.update_doc_id(tournament_data.doc_id)
    if(len(tournament.players) < 8):
        tournament = create_player_pool(tournament, 8 - len(tournament.players))
    tournament.update_tournament(tournament_data.doc_id)
    return tournament


def create_player_list(tournament):
    player_list = []
    for player_id in tournament.players:
        p_dict = model.search_player_by_doc_id(player_id)
        p = model.Player(lastname = p_dict['lastname'],firstname=p_dict['firstname'], birthdate=p_dict['birthdate'], sex=p_dict['sex'], total_score=p_dict['total_score'])
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
            print(p.doc_id)
            for r in tournament.rounds:
                for i in range(4):
                    if(r[i+3][0][0] == p.doc_id):
                        p.score += float(r[i+3][0][1])
                    if(r[i+3][1][0] == p.doc_id):
                        p.score += float(r[i+3][0][1])
            print(p.score)
            print('---------------------')
            #on récupère les points des joueurs selons les rounds qu'ils ont joué. 
            #Il s'agit maintenant de faire un classement dans une liste, en de vérifier s'ils n'ont pas déjà joué ensemble
        input()

        player_list.sort(key=lambda x: x.score, reverse=True)
    return player_list


def check_if_players_played_together(player1, player2):
    pass


def play_tournament(tournament):
    player_list = create_player_list(tournament)
    print(player_list)
    input()
    if(len(tournament.rounds) <= int(tournament.number_of_turns)):
        tournament.rounds.append(tournament.create_round(player_list))
    else:
        view.clear_terminal()
        print('Tournoi fini #todo')
        input()
    tournament.update_tournament(tournament.doc_id)


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
            input("Appuyez sur une touche pour continuer")
        elif choice == "5":
            view.display_tournaments(model.load_tournaments())
            input("Appuyez sur une touche pour continuer")
        elif choice == "6":
            edit_player()
        elif choice == "7":
            edit_tournament()
        elif choice == "8":
            play_tournament(t)
        elif choice == "0":
            break
        else:
            print("erreur : " + choice)


if __name__ == "__main__":
    main()
