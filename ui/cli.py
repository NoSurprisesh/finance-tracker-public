from ui.menus import user_login, get_menu_actions
from ui.cli_handlers import show_menus

WELCOME_EVENT = 'Welcome to my first finance app!'

MENU_PROMPT = ['Entry an income',
               'Entry an expense',
               'Show all entries',
               'Show balance',
               'Choose main currency',
               'Edit an entry',
               'Delete an entry',
               'Exit']


def start_program() -> None:
    print(WELCOME_EVENT)
    loaded_user = user_login()
    print(f'\nWelcome {loaded_user.username}!')
    while True:
        print()
        show_menus(MENU_PROMPT)
        choice = input(f'Chose a number from menu (1-{len(MENU_PROMPT)}):')
        menu_actions = get_menu_actions(loaded_user)
        if choice == '8':
            print('Exiting...')
            break
        elif choice in menu_actions:
            menu_actions[choice]()
        else:
            print('Invalid choice, please try again.')