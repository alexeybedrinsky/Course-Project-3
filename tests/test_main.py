import unittest
from unittest.mock import patch, mock_open
import json
from datetime import datetime
from src.main import format_operation  # Импорт из файла main.py в папке src



def test_format_operation():
    test_operation = {
        "date": "2022-05-15T08:30:00.000000",
        "from": "1234567890",
        "to": "0987654321",
        "operationAmount": {
            "amount": 100.50,
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Test operation"
    }

    expected_result = ("15.05.2022 Test operation\n"
                      "1234 XX** **** 7890 -> **** **** **** 4321\n"
                      "100.50 USD\n")

    result = format_operation(test_operation)

    result_lines = result.split('\n')
    result_amount = float(result_lines[2].split(' ')[0])

    expected_lines = expected_result.split('\n')
    expected_amount = float(expected_lines[2].split(' ')[0])

    assert round(result_amount, 2) == round(expected_amount, 2)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {
                "date": "2022-05-15T08:30:00.000000",
                "from": "1234567890",
                "to": "0987654321",
                "operationAmount": {
                    "amount": 100.50,
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Test operation",
                "state": "EXECUTED"
            },
            {
                "date": "2022-04-10T12:00:00.000000",
                "from": "1234567890",
                "to": "0987654321",
                "operationAmount": {
                    "amount": 200.75,
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Another operation",
                "state": "EXECUTED"
            },
            # Добавьте больше тестовых операций по необходимости
        ]

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {
            "date": "2022-05-15T08:30:00.000000",
            "from": "1234567890",
            "to": "0987654321",
            "operationAmount": {
                "amount": 100.50,
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Test operation",
            "state": "EXECUTED"
        },
        {
            "date": "2022-04-10T12:00:00.000000",
            "from": "1234567890",
            "to": "0987654321",
            "operationAmount": {
                "amount": 200.75,
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Another operation",
            "state": "EXECUTED"
        }
    ]))
    def test_read_file(self, mock_file):
        with open('operations.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.assertEqual(len(data), 2)


    def test_executed_operations(self):
        executed_operations = [operation for operation in self.test_data if 'state' in operation and operation['state'] == 'EXECUTED']
        self.assertEqual(len(executed_operations), 2)

    def test_last_5_executed_operations(self):
        executed_operations = [operation for operation in self.test_data if 'state' in operation and operation['state'] == 'EXECUTED']
        last_5_executed_operations = sorted(executed_operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)[:5]
        self.assertEqual(len(last_5_executed_operations), 2)
        self.assertEqual(last_5_executed_operations[0]['description'], 'Test operation')

if __name__ == '__main__':
    unittest.main()




