import os
import json
from core.models import UserData, Entry

def save_user_data_json(user_data: UserData) -> None:
    if not os.path.exists('data'):
        os.makedirs('data')

    user_entries = {
        'base_currency': user_data.base_currency,
        'incomes' : [entry.to_dict() for entry in user_data.incomes],
        'expenses' : [entry.to_dict() for entry in user_data.expenses],
    }

    file_path = os.path.join('data', f'{user_data.username}.json')

    with open(file_path, 'w') as file:
        json.dump(user_entries, file, indent=4)

def load_user_data_json(username: str) -> UserData:

    file_path = os.path.join('data', f'{username}.json')

    if not os.path.exists(file_path):
        return UserData(username)

    with open(file_path, 'r') as file:
        user_entries = json.load(file)

    user_data = UserData(username)
    user_data.base_currency = user_entries.get('base_currency', 'USD')
    user_data.incomes = [Entry.from_dict(entry) for entry in user_entries.get('incomes', [])]
    user_data.expenses = [Entry.from_dict(entry) for entry in user_entries.get('expenses', [])]

    return user_data











