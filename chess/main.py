#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB
import model


def show_players():
    db = TinyDB("players.json")
    view.show_player_list(db)


def add_player(prompted_player):
    player = model.Player(
        lastname=prompted_player['lastname'],
        firstname=prompted_player['firstname'],
        birthdate=prompted_player['birthdate'],
        sex=prompted_player['sex']
        )
    return player.insert_user()


def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    tournament = model.Tournament(
        name=prompted_tournament['name'],
        location=prompted_tournament['location'],
        date=prompted_tournament['date'],
        number_of_turns=prompted_tournament['number_of_turns'],
        instances=prompted_tournament['instances'],
        time_control=prompted_tournament['time_control'],
        description=prompted_tournament['description']
        )
    return tournament


def create_tournament():
    tournament = add_tournament()
    create_player_pool(tournament)


def create_player_pool(tournament):
    for i in range(1, 9):
        while True:
            choice = input(
                '0 créer joueur'
                '1 rechercher joueur')
            if(choice == '0'):
                view.clear_terminal()
                player_id = add_player(view.prompt_new_player())
                tournament.add_player(player_id)
                print('Player ' + str(i) + 'added')
                break
            elif(choice == '1'):  # search player then add him to the tournament
                lastname = input('lastname')
                model.search_players_by_lastname(lastname)
    tournament.insert_tournament()


def edit_player():
    lastname = input('lastname')
    player_id = view.select_player(model.search_players_by_lastname(lastname))
    model.update_player(view.prompt_new_player(), player_id)
    input("Joueur modifié avec succès. Appuyez sur une touche pour continuer")


def import_tournament():
    name = input('tournament name ?')
    tournament_data = view.select_tournament(model.search_tournament_by_name(name))
    input(tournament_data)
    t = model.Tournament(model.search_tournament_by_name(name))
    input(model.create_tournament_from_dict(t))


def main():
    while True:
        view.main_menu()
        choice = input("Choix de l'option :")
        if choice == "1":
            add_player(view.prompt_new_player())
        elif choice == "2":
            create_tournament()
        elif choice == "3":
            import_tournament()
        elif choice == "4":
            view.display_players(model.load_players())
            input("Appuyez sur une touche pour continuer")
        elif choice == "5":
            print("Liste des tournois")
        elif choice == "5":
            print("Modifier un joueur")
        elif choice == "6":
            edit_player()
        else:
            print("erreur : " + choice)


if __name__ == "__main__":
    main()
