import os
import requests
import json

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


def get_currency_data(base_currency: str = 'USD') -> dict:
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}'
    if not os.path.exists(f'exchange_data'):
        os.makedirs('exchange_data')
    file_path = (f'exchange_data/currency_'
                 f'{datetime.strftime(datetime.today(), '%Y_%m_%d')}_'
                 f'{base_currency}.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                currency_data = json.load(file)
                return currency_data
        except json.JSONDecodeError:
            os.remove(file_path)
            return get_currency_data(base_currency)
    else:
        with open(file_path, 'w') as file:

            response = requests.get(url)

            if response.status_code != 200:
                raise ConnectionError(f'Api error: {response.status_code}: {response.text}')

            currency_data = response.json()

            if not currency_data or not currency_data['result'] == 'success':
                raise ValueError('Invalid currency data: empty or malformed JSON.')
            if 'conversion_rates' not in currency_data:
                raise ValueError('Missing "conversion_rates" key in response.')

            json.dump(currency_data, file, indent=4)
            return currency_data


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return amount
    currency_data = get_currency_data(to_currency)
    rate = currency_data['conversion_rates'].get(from_currency)
    if not rate or rate == 0:
            raise ValueError(f'Invalid or zero rate from {from_currency} to {to_currency}')
    return amount / rate


