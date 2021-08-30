def menu_choice(choice):
    if choice == "1":
        print("Ajout de joueur")
    elif choice == "2":
        print("Création de tournoi")
    elif choice == "3":
        print("Importation de tournoi")
    elif choice == "4":
        print("Liste des joueurs")
    elif choice == "5":
        print("Liste des tournois")
    elif choice == "0":
        print("Quitter")
    else:
        print("erreur : " + choice)
