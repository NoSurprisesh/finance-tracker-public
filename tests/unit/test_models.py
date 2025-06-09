from datetime import datetime
from unittest import TestCase
from core.models import Entry

class TestEntry(TestCase):
    def test_to_dict(self):
        test_entry = Entry(
            flow_type='expenses',
            quantity=10,
            currency='USD',
            date=datetime(2020,1,1),
            category='Food',
            note='Pizza',
        )

        expected = {
            'flow_type': 'expenses',
            'quantity': 10,
            'currency': 'USD',
            'date': '2020-01-01',
            'category': 'Food',
            'note': 'Pizza',
        }

        self.assertEqual(expected, test_entry.to_dict())

    def test_from_dict(self):
        test_json = {
            'flow_type': 'expenses',
            'quantity': 10,
            'currency': 'USD',
            'date': '2020-01-01',
            'category': 'Food',
            'note': 'Pizza',
        }
        new_entry = Entry.from_dict(test_json)

        self.assertEqual(new_entry.flow_type, 'expenses')
        self.assertEqual(new_entry.quantity, 10)
        self.assertEqual(new_entry.category, 'Food')
        self.assertEqual(new_entry.note, 'Pizza')
        self.assertEqual(new_entry.date, datetime(2020,1,1))
        self.assertEqual(new_entry.category, 'Food')
        self.assertEqual(new_entry.note, 'Pizza')





