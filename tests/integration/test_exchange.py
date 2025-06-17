import json
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock, ANY

import requests

from core.exchange import get_currency_data, convert_currency


class TestExchange(TestCase):
    @patch('builtins.open',
           new_callable=mock_open,
           read_data='{"result": "success", "conversion_rates": {"EUR": 0.85}}')
    @patch('os.path.exists',
           return_value=True)
    def test_existing_valid_file(self,
                                 mock_exists,
                                 mock_open_file):
        data = get_currency_data('USD')
        self.assertIn('conversion_rates', data)
        self.assertEqual(data['result'], 'success')

    @patch('json.load',
           side_effect=json.JSONDecodeError('Expecting value',
                                            'doc',
                                            0))
    @patch('requests.get')
    @patch('os.path.exists',
           side_effect=(True,
                        True,
                        True,
                        False))
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_broken_json_file(self,
                              mock_remove,
                              mock_open_file,
                              mock_exists,
                              mock_get,
                              mock_load_json):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {"EUR": 0.85}
        }
        mock_get.return_value = mock_response

        data = get_currency_data('USD')

        self.assertEqual(data['conversion_rates']['EUR'], 0.85)
        mock_remove.assert_called_once()

    @patch('os.path.exists', side_effect=(True, False))
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    @patch('json.dump')
    def test_currency_data_request(self,
                                   mock_dump,
                                   mock_request,
                                   mock_open_file,
                                   mock_exists ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": "success",
            "conversion_rates": {"EUR": 0.85}
        }
        mock_request.return_value = mock_response

        expected_data = get_currency_data('USD')

        file = mock_open_file.return_value

        mock_request.assert_called_once()
        mock_open_file.assert_called_once_with(ANY, 'w')
        mock_dump.assert_called_once_with(expected_data, file, indent=4)
        self.assertEqual(expected_data['conversion_rates']['EUR'], 0.85)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', side_effect=(True, False))
    @patch('requests.get')
    def test_response_status_code(self,
                                  mock_get,
                                  mock_exists,
                                  mock_open_file):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError) as cm:
            get_currency_data('USD')

        self.assertEqual('Api error: 500: Internal Server Error',
                         str(cm.exception))

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', side_effect=(True, False, True, False))
    @patch('requests.get')
    def test_get_currency_data_value_error_invalid_result(self,
                                           mock_get,
                                           mock_exists,
                                           mock_open_file):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        mock_response.json.return_value = {
            "result": "error",
            "conversion_rates": {"EUR": 0.85}
        }

        with self.assertRaises(ValueError) as cm:
            get_currency_data('USD')
        self.assertEqual(
            'Invalid currency data: empty or malformed JSON.',
            str(cm.exception)
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', side_effect=(True, False, True, False))
    @patch('requests.get')
    def test_get_currency_data_value_error_missing_conversion_rates(self,
                                           mock_get,
                                           mock_exists,
                                           mock_open_file):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        mock_response.json.return_value = {
            "result": "success",
            "test": {"EUR": 0.85}
        }

        with self.assertRaises(ValueError) as cm:
            get_currency_data('USD')
        self.assertEqual(
            'Missing "conversion_rates" key in response.',
            str(cm.exception)
        )

    def test_convert_currency_equal_args(self):
        with patch('core.exchange.get_currency_data',) as mock_get_currency_data:
            expected_amount = 100

            self.assertEqual(expected_amount,
                            convert_currency(100,
                                             'USD',
                                             'USD'))
            self.assertEqual(expected_amount,
                            convert_currency(100,
                                             'EUR',
                                             'EUR'))


    def test_convert_currency_not_equal_args(self):
        with patch('core.exchange.get_currency_data') as mock_get_currency_data:
            mock_get_currency_data.return_value = {
                'conversion_rates': {'USD': 2,
                                     'PLN': 4}
            }
            expected_amount = 50
            expected_amount2 = 25

            self.assertEqual(expected_amount,
                             convert_currency(100,
                                              'USD',
                                              'EUR'))
            self.assertEqual(expected_amount2,
                             convert_currency(100,
                                              'PLN',
                                              'EUR'))

    def test_convert_currency_raise_value_error(self):
        with patch('core.exchange.get_currency_data') as mock_get_currency_data:
            mock_get_currency_data.return_value = {
                'conversion_rates': {'USD': 0,
                                     'EUR': ''}
            }

            with self.assertRaises(ValueError) as cm:
                convert_currency(100,
                                 'USD',
                                 'PLN')
            self.assertEqual('Invalid or zero rate from USD to PLN',
                                 str(cm.exception))
            with self.assertRaises(ValueError) as cm:
                convert_currency(100,
                                 'EUR',
                                 'USD')
            self.assertEqual('Invalid or zero rate from EUR to USD',
                             str(cm.exception))