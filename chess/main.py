#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB
from model import Player, Tournament

def show_players():
    db = TinyDB("players.json")
    return view.show_player_list(db)

def add_player():
    prompted_player = view.prompt_new_player()
    print(prompted_player)
    player = Player(lastname=prompted_player['lastname'], 
                        firstname=prompted_player['firstname'],
                        birthdate=prompted_player['birthdate'], 
                        sex=prompted_player['sex'], 
                        elo=prompted_player['elo'])
    return player.insert_user()

def add_tournament():
    prompted_tournament = view.prompt_new_tournament()
    print(prompted_tournament)
    tournament = Tournament(name = prompted_tournament['name'], 
                            location = prompted_tournament['location'], 
                            date = prompted_tournament['date'], 
                            number_of_turns = prompted_tournament['number_of_turns'], 
                            instances = prompted_tournament['instances'], 
                            time_control = prompted_tournament['time_control'], 
                            description = prompted_tournament['description'])
    return tournament.insert_tournament()

def create_tournament():
    while True:
        delete_tournament = input("Attention, vous allez perdre les dernières données enregistrées.\n"
                                    "0: Quitter en conservant les données\n"
                                    "1: Ecraser les données et continuer\n"
                                    "Saisissez votre choix : ")
        if delete_tournament == "0":
            break
        elif delete_tournament == "1":
            add_tournament()
            create_player_pool()
        else:
            print("Erreur de saisie.\n")

def create_player_pool():
    pass

def main():
    while True:
        view.main_menu()
        choice = input("Choix de l'option :")
        if choice == "1":
            add_player()
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