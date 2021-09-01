#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB
from model import Player

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

def main():
    view.main_menu()
    choice = input("Choix de l'option :")
    if choice == "1":
        add_player()
    elif choice == "2":
        print("Création de tournoi")
    elif choice == "3":
        print("Importation de tournoi")
    elif choice == "4":
        return show_players()
    elif choice == "5":
        print("Liste des tournois")
    elif choice == "0":
        print("Quitter")
    else:
        print("erreur : " + choice)


if __name__ == "__main__":
    main()