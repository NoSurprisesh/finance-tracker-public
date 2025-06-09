import os

from datetime import datetime

from core.models import UserData, Entry
from core.storage import save_user_data_json, load_user_data_json


WELCOME_EVENT = 'Welcome to my first finance app!'


MENU_PROMPT = ['Entry an income',
               'Entry an expense',
               'Show all entries',
               'Show balance',
               'Exit']


def show_menu() -> None:
    for index, item in enumerate(MENU_PROMPT, start=1):
        print(f'{index}. {item}')


def user_login() -> UserData:
    while True:
        user_name = input('Enter user name for log in:').strip()
        if user_name == '':
            print('User name must not be empty')
        elif os.path.exists(f'data/{user_name}.json'):
            return load_user_data_json(user_name)
        else:
            choice = input(f'User name does not exist.\n'
                        f'If you want to create new one with name "{user_name}" enter "y". \n'
                        f'If you want to enter another user name enter anything else.').strip().lower()
            if choice == 'y':
                new_user = UserData(user_name)
                save_user_data_json(new_user)
                return new_user


def start_program() -> None:
    print(WELCOME_EVENT)
    loaded_user = user_login()
    print(f'Welcome {loaded_user.username}!')
    while True:
        show_menu()
        choice = input('Chose a number from menu (1-5):')
        if choice not in [str(i+1) for i in range(len(MENU_PROMPT))]:
            print('Invalid input, select only menu numbers')
        else:
            if choice == '1':
                entry_input(loaded_user, 'income')
            elif choice == '2':
                entry_input(loaded_user, 'expense')
            elif choice == '3':
                show_all_entries(loaded_user)
            elif choice == '4':
                show_balance(loaded_user)
            elif choice == '5':
                print('Exiting...')
                break


def entry_input(user: UserData, flow_type: str) -> None:
    if flow_type not in ('income', 'expense'):
        raise ValueError(f'Unknown flow_type: {flow_type}')
    while True:
        print(f'Creating new {flow_type} entry...')
        while True:
            try:
                quantity = float(input(f'Enter the {flow_type} amount:').strip())
                break
            except ValueError:
                print('Invalid input, enter numeric only, try again.')

        currency = input(f'Enter the {flow_type} currency:').strip()

        while True:
            try:
                date = datetime.strptime(input(
                    f'Enter the {flow_type} date in format YYYY-MM-DD:'
                ).strip(),'%Y-%m-%d')
                break
            except ValueError:
                    print('Invalid input, enter string data in format YYYY-MM-DD, try again.')

        category = input(f'Enter the {flow_type} category:').strip()

        note = input(f'Enter the {flow_type} note:').strip()

        new_entry = Entry(flow_type,
                          quantity,
                          currency,
                          date,
                          category,
                          note)
        print()
        if input(f'Check the inputted data:\n'
                 f'{new_entry.to_dict()}\n'
                 f'If everything is correct press "y"').strip().lower() == 'y':

            user.add_entry(new_entry)
            save_user_data_json(user)
            print(f'{flow_type.capitalize()} entry added.')
            break
        else:
            print("Entry cancelled. Let's try again")


def show_all_entries(user: UserData) -> None:
    entries = {'incomes': user.incomes, 'expenses': user.expenses}
    print(f'Showing all {user.username} entries...\n')
    for k,v in entries.items():
        print(f'--- {k.capitalize()} ---')
        if not v:
            print(f'There are no {k} yet')
        else:
            for item in v:
                print(f'[{item.date.strftime('%Y-%m-%d')}] {item.quantity} {item.currency}'
                    f' - {item.category.capitalize()}: (Note:{item.note})')
    input('\nPress ENTER to return to main menu...')


def show_balance(user) -> None:
    if not user.incomes and not user.expenses:
        print('No entries to calculate balance')
    else:
        balance = user.get_balance()
        currency = (user.incomes[0].currency if user.incomes else user.expenses[0].currency)
        print(f'Your current balance is: '
              f'{'+' if balance > 0 else '' if balance == 0 else '-'}'
              f'{abs(balance):.2f} {currency}')
    print('\nPress ENTER to return to main menu...')


if __name__ == '__main__':
    start_program()