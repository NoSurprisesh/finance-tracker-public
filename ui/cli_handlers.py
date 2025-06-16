from core.storage import save_user_data_json, load_user_data_json
from core.models import UserData, Entry
from core.exchange import get_currency_data
from datetime import datetime


EDIT_PROMPT = ['Edit incomes', 'Edit expenses','Back to main menu']

DELETE_PROMPT = ['Delete income', 'Delete expense', 'Back to main menu']

def show_menus(prompt) -> None:
    for index, item in enumerate(prompt, start=1):
        print(f'{index}. {item}')


def save_new_entry(user: UserData, flow_type: str) -> None:
    new_entry = entry_input(flow_type)
    user.add_entry(new_entry)
    save_user_data_json(user)
    print(f'{flow_type.capitalize()} entry added.')


def entry_input(flow_type: str, edit: bool = False) -> Entry:
    if flow_type not in ('income', 'expense'):
        raise ValueError(f'Unknown flow_type: {flow_type}')
    currency_data = get_currency_data()
    while True:
        print(f'{'Editing' if edit else 'Create new'} {flow_type} entry...')
        while True:
            try:
                quantity = float(input(f'Enter the {flow_type} amount:').strip())
                break
            except ValueError:
                print('Invalid input, enter numeric only, try again.')
        while True:
            currency = input(f'Enter the {flow_type} currency:').strip().upper()
            if currency in currency_data['conversion_rates']:
                break
            print(f'Currency data for {currency} not found.')
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
            return new_entry
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


def show_part_of_entries(user: UserData, choice: str) -> dict:
    entry_groups = {'1': user.incomes, '2': user.expenses}
    for index, item in enumerate(entry_groups[choice], start=1):
        print(f'{index}. [{item.date.strftime('%Y-%m-%d')}] {item.quantity} {item.currency}'
              f' - {item.category.capitalize()}: (Note:{item.note})')
    return entry_groups[choice]


def show_balance(user: UserData) -> None:
    if not user.incomes and not user.expenses:
        print('No entries to calculate balance')
    else:
        balance = user.get_balance()
        currency = user.base_currency
        print(f'Your current balance is: '
              f'{'+' if balance > 0 else '' if balance == 0 else '-'}'
              f'{abs(balance):.2f} {currency}')
    input('\nPress ENTER to return to main menu...')


def choose_base_currency(user: UserData) -> None:
    while True:
        base_currency = input('Enter the base currency:').strip().upper()
        if base_currency == user.base_currency:
            print(f'Your base currency already {user.base_currency}!')
            return
        currency_data = get_currency_data()
        if base_currency in currency_data['conversion_rates']:
            user.base_currency = base_currency
            save_user_data_json(user)
            print(f'{base_currency} is base currency now.')
            break
        print(f'Currency data for {base_currency} not found.')
    input('\nPress ENTER to return to main menu...')


def edit_entry(user: UserData) -> None:
    while True:
        show_menus(EDIT_PROMPT)
        choice = input('Enter menu number:').strip()
        if choice in map(str, range(1, len(EDIT_PROMPT) + 1)):
            if choice in ['1', '2']:
                dict_entry = show_part_of_entries(user, choice)
                while True:
                    try:
                        entry_index = int(input(f'Enter the entry number to edit:').strip())
                        if entry_index-1 in range(len(dict_entry)):
                            flow_type = dict_entry[0].flow_type
                            new_entry = entry_input(flow_type, True)
                            user.edit_entry(entry_index-1, flow_type, new_entry)
                            print(f'Entry {entry_index} edited. ')
                            break
                        else:
                            print(f'Entry {entry_index} not found.')
                    except ValueError:
                        print('Invalid input, enter valid number of entry.')
            if choice == '3':
                return
        else:
            print('Invalid input, enter numeric only, try again.')


def delete_entry(user: UserData) -> None:
    while True:
        show_menus(DELETE_PROMPT)
        choice = input('Enter menu number:').strip()
        if choice in map(str, range(1, len(DELETE_PROMPT) + 1)):
            if choice in ['1', '2']:
                dict_entry = show_part_of_entries(user, choice)
                while True:
                    try:
                        removal_index = int(input(f'Enter the entry number to remove:').strip())
                        if removal_index-1 in range(len(dict_entry)):
                            user.remove_entry(removal_index-1, dict_entry[removal_index-1].flow_type)
                            save_user_data_json(user)
                            print(f'Entry {removal_index} removed.')
                            break
                        else:
                            print(f'Entry {removal_index} not found.')
                    except ValueError:
                        print('Invalid input, enter valid number of entry.')
            if choice == '3':
                return
        else:
            print('Invalid input, enter numeric only, try again.')