def menu_choice(choice):
    match choice:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return 4
        case 5:
            return 5
        case 0:
            return 6
        case _:        
            return 0   # 0 is the default case if x is not found