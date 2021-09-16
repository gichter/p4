#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB
from model import Player, Tournament


def show_players():
    db = TinyDB("players.json")
    return view.show_player_list(db)


def create_player(player_number):
    prompted_player = view.prompt_new_player(player_number)
    player = Player(lastname=prompted_player['lastname'],
                    firstname=prompted_player['firstname'],
                    birthdate=prompted_player['birthdate'],
                    sex=prompted_player['sex'])
    player.insert_player()
    return player


def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    tournament = Tournament(name=prompted_tournament['name'],
                            location=prompted_tournament['location'],
                            date=prompted_tournament['date'],
                            number_of_turns=prompted_tournament['number_of_turns'],
                            instances=prompted_tournament['instances'],
                            time_control=prompted_tournament['time_control'],
                            description=prompted_tournament['description'])
    tournament.insert_tournament()
    return tournament


def create_tournament():
    view.clear_terminal()
    while True:
        delete_tournament = input(
            "Attention, vous allez perdre les dernières données enregistrées.\n"
            "0: Quitter en conservant les données\n"
            "1: Ecraser les données et continuer\n"
            "Saisissez votre choix : ")
        if delete_tournament == "0":
            break
        elif delete_tournament == "1":
            tournament = add_tournament()
            create_player_pool(tournament)
        else:
            print("Erreur de saisie.\n")


def create_player_pool(tournament):
    for player_number in range(1, 9):
        view.clear_terminal()
        player = create_player(player_number)
        tournament.add_player(player)


def main():
    while True:
        view.main_menu()
        choice = input("Choix de l'option :")
        if choice == "1":
            create_player(0)
        elif choice == "2":
            create_tournament()
        elif choice == "3":
            print("Importation de tournoi")
        elif choice == "4":
            print("liste des joueurs")
        elif choice == "5":
            print("Liste des tournois")
        elif choice == "0":
            break
        else:
            print("erreur : " + choice)


if __name__ == "__main__":
    main()
