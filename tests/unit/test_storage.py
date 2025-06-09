from unittest import TestCase
from datetime import datetime
from core.storage import *

class TestStorage(TestCase):
    def test_save_and_load_user_data(self):
        test_user = UserData('test_user')

        income_entry = Entry(
            flow_type='income',
            quantity=10,
            currency='USD',
            date=datetime(2020,1,1),
            category='Freelance',
            note='C',
        )

        expense_entry = Entry(
            flow_type='expense',
            quantity=9,
            currency='USD',
            date=datetime(2020, 1, 2),
            category='Food',
            note='Bueno'
        )

        test_user.add_entry(income_entry)
        test_user.add_entry(expense_entry)
        test_user.add_entry(expense_entry)

        save_user_data_json(test_user)

        loaded_user_data = load_user_data_json(test_user.username)

        self.assertEqual(test_user.username, loaded_user_data.username)
        self.assertEqual(income_entry.to_dict(), loaded_user_data.incomes[0].to_dict())
        self.assertEqual(test_user.expenses[0].category, loaded_user_data.expenses[0].category)
        self.assertEqual(len(loaded_user_data.incomes), 1)
        self.assertEqual(len(loaded_user_data.expenses), 2)
        self.assertEqual(loaded_user_data.expenses[0].date, datetime(2020, 1, 2))




    def tearDown(self):
        file_path = 'data/test_user.json'
        if os.path.exists(file_path):
            os.remove(file_path)

