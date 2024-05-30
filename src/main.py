import os
import json
from datetime import datetime


def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)


def load_operations(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def format_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')


def mask_account(account):
    if any(card_type in account for card_type in ["Visa", "MasterCard", "Maestro"]):
        card_type = "Visa" if "Visa" in account else ("MasterCard" if "MasterCard" in account else "Maestro")
        card_number = account.split()[-1]
        masked_number = card_number[:6] + "*" * (len(card_number) - 10) + card_number[-4:]
        grouped_masked_number = ' '.join([masked_number[i:i+4] for i in range(0, len(masked_number), 4)])
        return f"{card_type} {grouped_masked_number}"
    elif "Счет" in account:
        account_number = account.split()[-1]
        masked_account_number = "**" + account_number[-4:]
        return f"Счет {masked_account_number}"
    return account




def format_operation(operation):
    date = format_date(operation['date'])
    from_account = mask_account(operation.get('from', 'Не указано'))
    to_account = mask_account(operation.get('to', 'Не указано'))

    try:
        amount = float(operation['operationAmount']['amount'])
    except ValueError:
        amount = 0.0

    formatted_amount = f"{amount:.2f}"  # Форматируем сумму с двумя знаками после запятой
    currency = operation['operationAmount']['currency']['name']
    description = operation['description']

    return f"{date} {description}\n{from_account} -> {to_account}\n{formatted_amount} {currency}\n"


def get_executed_operations(data):
    return [operation for operation in data if 'state' in operation and operation['state'] == 'EXECUTED']


def get_last_5_executed_operations(operations):
    return sorted(operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)[:5]


def main():
    file_path = get_file_path('operations.json')
    data = load_operations(file_path)
    executed_operations = get_executed_operations(data)
    last_5_executed_operations = get_last_5_executed_operations(executed_operations)

    for operation in last_5_executed_operations:
        print(format_operation(operation))


if __name__ == '__main__':
    main()

