from view.menus import main_menu
from controller.menu import menu_choice

def main():
    choice = main_menu()
    menu_choice(choice)


if __name__ == "__main__":
    main()