import unittest
from src.main import format_operation, mask_account


class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_data = self.create_test_data()

    def create_test_data(self):
        return [
            {
                "date": "2022-05-15T08:30:00.000000",
                "from": "Visa Platinum 1234567890123456",
                "to": "Счет 0000000000000000",
                "operationAmount": {
                    "amount": "100.50",
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
                "from": "Visa 1234567890123456",
                "to": "MasterCard 6543210987654321",
                "operationAmount": {
                    "amount": "200.75",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Another operation",
                "state": "EXECUTED"
            },
            {
                "date": "2019-11-19T08:30:00.000000",
                "from": "Maestro 7810846596785568",
                "to": "Счет 0000000000002869",
                "operationAmount": {
                    "amount": "30153.72",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "state": "EXECUTED"
            }
        ]

    def test_mask_account_card(self):
        card_account = "Visa Platinum 1234567890123456"
        masked_card_account = mask_account(card_account)
        expected_masked_card_account = "Visa 1234 56** **** 3456"
        self.assertEqual(masked_card_account, expected_masked_card_account)

    def test_mask_account_bank(self):
        bank_account = "Счет 0000000000000000"
        masked_bank_account = mask_account(bank_account)
        expected_masked_bank_account = "Счет **0000"
        self.assertEqual(masked_bank_account, expected_masked_bank_account)

    def test_mask_account_maestro(self):
        maestro_account = "Maestro 7810846596785568"
        masked_maestro_account = mask_account(maestro_account)
        expected_masked_maestro_account = "Maestro 7810 84** **** 5568"
        self.assertEqual(masked_maestro_account, expected_masked_maestro_account)

    def test_format_operation(self):
        test_operation = self.test_data[0]

        expected_result_lines = [
            "15.05.2022 Test operation",
            "Visa 1234 56** **** 3456 -> Счет **0000",
            "100.50 USD"
        ]

        result = format_operation(test_operation)
        result_lines = result.strip().split('\n')

        self.assertEqual(result_lines[0], expected_result_lines[0])
        self.assertEqual(result_lines[1], expected_result_lines[1])
        self.assertAlmostEqual(float(result_lines[2].split(' ')[0]), float(expected_result_lines[2].split(' ')[0]),
                               places=2)
        self.assertEqual(result_lines[2].split(' ')[1], expected_result_lines[2].split(' ')[1])

    def test_format_operation_another(self):
        test_operation = self.test_data[1]

        expected_result_lines = [
            "10.04.2022 Another operation",
            "Visa 1234 56** **** 3456 -> MasterCard 6543 21** **** 4321",
            "200.75 USD"
        ]

        result = format_operation(test_operation)
        result_lines = result.strip().split('\n')

        self.assertEqual(result_lines[0], expected_result_lines[0])
        self.assertEqual(result_lines[1], expected_result_lines[1])
        self.assertAlmostEqual(float(result_lines[2].split(' ')[0]), float(expected_result_lines[2].split(' ')[0]),
                               places=2)
        self.assertEqual(result_lines[2].split(' ')[1], expected_result_lines[2].split(' ')[1])

    def test_format_operation_maestro(self):
        test_operation = self.test_data[2]

        expected_result_lines = [
            "19.11.2019 Перевод организации",
            "Maestro 7810 84** **** 5568 -> Счет **2869",
            "30153.72 руб."
        ]

        result = format_operation(test_operation)
        result_lines = result.strip().split('\n')

        self.assertEqual(result_lines[0], expected_result_lines[0])
        self.assertEqual(result_lines[1], expected_result_lines[1])
        self.assertAlmostEqual(float(result_lines[2].split(' ')[0]), float(expected_result_lines[2].split(' ')[0]),
                               places=2)
        self.assertEqual(result_lines[2].split(' ')[1], expected_result_lines[2].split(' ')[1])

    def test_mask_account_invalid(self):
        invalid_account = "Счет Invalid Account"
        masked_account = mask_account(invalid_account)
        expected_masked_account = "Счет **ount"
        self.assertEqual(masked_account, expected_masked_account)

    def test_format_operation_invalid(self):
        invalid_operation = {
            "date": "2022-05-15T08:30:00.000000",
            "from": "Счет Invalid Account",
            "to": "Счет Invalid Account",
            "operationAmount": {
                "amount": "0.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Invalid operation",
            "state": "FAILED"
        }

        expected_result_lines = [
            "15.05.2022 Invalid operation",
            "Счет **ount -> Счет **ount",
            "0.00 USD"
        ]

        result = format_operation(invalid_operation)
        result_lines = result.strip().split('\n')

        self.assertEqual(result_lines[0], expected_result_lines[0])
        self.assertEqual(result_lines[1], expected_result_lines[1])
        self.assertAlmostEqual(float(result_lines[2].split(' ')[0]), float(expected_result_lines[2].split(' ')[0]),
                               places=2)
        self.assertEqual(result_lines[2].split(' ')[1], expected_result_lines[2].split(' ')[1])


if __name__ == '__main__':
    unittest.main()
