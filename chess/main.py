#! /usr/bin/env python3
# coding: utf-8

from view import prompt_new_player
import view
from tinydb import TinyDB
from model import Player, Tournament


def show_players():
    db = TinyDB("players.json")
    view.show_player_list(db)


def add_player(prompted_player):
    player = Player(lastname=prompted_player['lastname'],
                    firstname=prompted_player['firstname'],
                    birthdate=prompted_player['birthdate'],
                    sex=prompted_player['sex']
                    )
    return player.insert_user()


def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    tournament = Tournament(name=prompted_tournament['name'],
                            location=prompted_tournament['location'],
                            date=prompted_tournament['date'],
                            number_of_turns=prompted_tournament['number_of_turns'],
                            instances=prompted_tournament['instances'],
                            time_control=prompted_tournament['time_control'],
                            description=prompted_tournament['description'])
#    tournament.insert_tournament()
    return tournament


def create_tournament():
    tournament = add_tournament()
    create_player_pool(tournament)


def create_player_pool(tournament):
    for i in range(1, 9):
        while True:
            choice = input('0 créer joueur'
                           '1 rechercher joueur')
            if(choice == '0'):
                view.clear_terminal()
                player_id = add_player(view.prompt_new_player())
                tournament.add_player(player_id)
                print('Player ' + str(i) + 'added')
                break
            elif(choice == '1'):  # search player then add him to the tournament
                pass
    tournament.insert_tournament()


def main():
    while True:
        view.main_menu()
        choice = input("Choix de l'option :")
        if choice == "1":
            add_player(view.prompt_new_player())
        elif choice == "2":
            create_tournament()
        elif choice == "3":
            print("Importation de tournoi")
        elif choice == "4":
            show_players()
        elif choice == "5":
            print("Liste des tournois")
        elif choice == "5":
            print("Récupérer le dernier tournoi en cours")
        elif choice == "6":
            break
        else:
            print("erreur : " + choice)


if __name__ == "__main__":
    main()
