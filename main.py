import json

def display_last_executed_operations(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        executed_operations = [operation for operation in data if 'status' in operation and operation['status'] == 'EXECUTED']
        sorted_operations = sorted(executed_operations, key=lambda x: x.get('date', 0), reverse=True)

        for operation in sorted_operations[:5]:
            print(f"Дата: {operation.get('date', 'Unknown')}")
            print(f"Описание: {operation.get('description', 'Unknown')}")
            print(f"Счет отправителя: {operation.get('from_account', 'Unknown')}")
            print(f"Сумма: {operation.get('amount', 'Unknown')} {operation.get('currency', 'Unknown')}")
            print("-----------------------\n")

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка при чтении файла {file_path}. Проверьте формат JSON.")

display_last_executed_operations("operations.json")