from unittest import TestCase
from unittest.mock import patch, call
from ui.cli_handlers import *

class TestCliHandlers(TestCase):
    def setUp(self):
        self.test_user = UserData('Test')

    @patch('builtins.input', side_effect=['USD', 'y'])
    @patch('builtins.print')
    def test_choose_base_currency_same_as_inputted(self,
                                                   mock_print,
                                                   mock_input):
        choose_base_currency(self.test_user)
        mock_print.assert_called_once_with('Your base currency already USD!')

    @patch('ui.cli_handlers.get_currency_data',
           return_value={'conversion_rates':
                             {
                                 'PLN': 0.5
                             }})
    @patch('ui.cli_handlers.save_user_data_json')
    @patch('builtins.input', side_effect=['PLN', 'y'])
    @patch('builtins.print')
    def test_choose_base_currency_different_from_inputted(self,
                                                          mock_print,
                                                          mock_input,
                                                          mock_save_user_data,
                                                          mock_get_currency):

        self.assertEqual(self.test_user.base_currency, 'USD')

        choose_base_currency(self.test_user)

        self.assertEqual(self.test_user.base_currency, 'PLN')
        mock_print.assert_called_once_with('PLN is base currency now.')
        mock_save_user_data.assert_called_once_with(self.test_user)

    @patch('ui.cli_handlers.get_currency_data',
           return_value={'conversion_rates':
                             {
                                 'PLN': 0.5
                             }})
    @patch('ui.cli_handlers.save_user_data_json')
    @patch('builtins.input', side_effect=['TEST', 'PLN', 'y'])
    @patch('builtins.print')
    def test_choose_base_currency_base_currency_not_found(self,
                                                           mock_print,
                                                           mock_input,
                                                           mock_save_user_data,
                                                           mock_get_currency):
        choose_base_currency(self.test_user)

        mock_print.assert_has_calls([
            call('Currency data for TEST not found.'),
            call('PLN is base currency now.')
        ])
        self.assertEqual(mock_input.call_count, 3)










