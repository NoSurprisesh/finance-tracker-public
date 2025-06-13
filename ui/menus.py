import os

from typing import Callable
from core.models import UserData
from core.storage import load_user_data_json, save_user_data_json
from ui.cli_handlers import (save_new_entry, show_all_entries,
                             show_balance, choose_base_currency,
                             edit_entry, delete_entry)


def user_login() -> UserData:
    while True:
        user_name = input('Enter user name for log in:').strip().lower()
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


def get_menu_actions(user: UserData) -> dict[str, Callable[[], None]]:
    return {
        '1': lambda: save_new_entry(user, 'income'),
        '2': lambda: save_new_entry(user, 'expense'),
        '3': lambda: show_all_entries(user),
        '4': lambda: show_balance(user),
        '5': lambda: choose_base_currency(user),
        '6': lambda: edit_entry(user),
        '7': lambda: delete_entry(user),
    }