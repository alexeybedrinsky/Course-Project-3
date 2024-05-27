import json
from datetime import datetime

# Чтение данных из файла operations.json
with open('operations.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def format_operation(operation):
    date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    from_account = operation.get('from', 'Не указано')
    masked_from_account = ' '.join([from_account[:4], 'XX**', '****', from_account[-4:]]) if from_account != 'Не указано' else ''
    masked_to_account = f'**** **** **** {operation["to"][-4:]}'
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']
    description = operation['description']
    return f"{date} {description}\n{masked_from_account} -> {masked_to_account}\n{amount} {currency}\n"

executed_operations = [operation for operation in data if 'state' in operation and operation['state'] == 'EXECUTED']
last_5_executed_operations = sorted(executed_operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)[:5]

for operation in last_5_executed_operations:
    print(format_operation(operation))
