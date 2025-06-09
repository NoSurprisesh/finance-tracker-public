from datetime import datetime
from unittest import TestCase
from core.models import UserData, Entry

class TestUserData(TestCase):
    def make_entry(self,
                   flow_type='income',
                   quantity=100.0,
                   currency='USD',
                   date=datetime(2025, 1, 1),
                   category='Test category',
                   note='Test Note'
        ):
        return Entry(
            flow_type=flow_type,
            quantity=quantity,
            currency=currency,
            date=date,
            category=category,
            note=note
        )

    def test_add_entry_income(self):
        user_data = UserData('TestName')

        test_income_entry = self.make_entry(flow_type = 'income',
                                            category = 'Food')

        user_data.add_entry(test_income_entry)

        self.assertEqual(len(user_data.incomes), 1)
        self.assertEqual(len(user_data.expenses), 0)
        self.assertEqual(user_data.incomes[0].category, 'Food')

    def test_add_entry_expense(self):
        user_data = UserData('TestName')

        test_income_entry = self.make_entry(flow_type = 'expense',
                                            note = 'Cups ')

        user_data.add_entry(test_income_entry)

        self.assertEqual(len(user_data.expenses), 1)
        self.assertEqual(len(user_data.incomes), 0)
        self.assertEqual(user_data.expenses[0].note, 'Cups ')

    def test_get_balance(self):
        user_data = UserData('TestName')

        income_entry1 = self.make_entry(flow_type = 'income',
                                        quantity = 50.0)
        income_entry2 = self.make_entry(flow_type = 'income',
                                        quantity = 15.5)
        expense_entry1 = self.make_entry(flow_type = 'expense',
                                         quantity = 16.5)
        expense_entry2 = self.make_entry(flow_type = 'expense',
                                         quantity = 48.0)

        user_data.add_entry(income_entry1)
        user_data.add_entry(income_entry2)
        user_data.add_entry(expense_entry1)
        user_data.add_entry(expense_entry2)

        balance = user_data.get_balance()

        self.assertEqual(balance, 1)

    def test_edit_entry(self):
        user_data = UserData('TestName')

        income_entry = self.make_entry(flow_type = 'income',)
        income_entry_edited = self.make_entry(flow_type = 'income', currency = 'PLN')
        income_entry_edited2 = self.make_entry(flow_type = 'income', quantity = 1)

        user_data.add_entry(income_entry)
        user_data.edit_entry(0,'income',income_entry_edited)

        self.assertEqual(len(user_data.incomes), 1)
        self.assertEqual(user_data.incomes[0].currency, income_entry_edited.currency)

        user_data.edit_entry(0,'income',income_entry_edited2)

        self.assertEqual(user_data.incomes[0].currency, income_entry_edited2.currency)
        self.assertEqual(user_data.incomes[0].quantity, income_entry_edited2.quantity)

    def test_remove_entry(self):
        user_data = UserData('TestName')

        income_entry = self.make_entry(flow_type = 'income',)
        income_entry2 = self.make_entry(flow_type = 'income', quantity = 1)
        expense_entry = self.make_entry(flow_type = 'expense',)
        expense_entry2 = self.make_entry(flow_type = 'expense', quantity = 16.5)

        user_data.add_entry(income_entry)
        user_data.add_entry(expense_entry)
        user_data.add_entry(expense_entry2)
        user_data.add_entry(income_entry2)

        self.assertEqual(len(user_data.incomes), 2)
        self.assertEqual(len(user_data.expenses), 2)

        user_data.remove_entry(1, 'income')

        self.assertEqual(len(user_data.incomes), 1)
        self.assertEqual(len(user_data.expenses), 2)
        self.assertEqual(user_data.incomes[0].quantity, 100)

        user_data.remove_entry(0, 'income')
        user_data.remove_entry(0, 'expense')

        self.assertEqual(len(user_data.incomes), 0)
        self.assertEqual(len(user_data.expenses), 1)
        self.assertEqual(user_data.expenses[0].quantity, 16.5)







