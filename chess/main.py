#! /usr/bin/env python3
# coding: utf-8

import view
from tinydb import TinyDB

def show_players():
    db = TinyDB("players.json")
    return view.show_player_list(db)

def main():
    view.main_menu()
    choice = "4"#input("Choix de l'option :")
    if choice == "1":
        print("Ajout de joueur")
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