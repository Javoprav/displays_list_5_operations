'''импорты и переменные(константы)'''
import requests, json, os

URL_LIST_OPERATIONS = 'https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230131%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230131T111731Z&X-Amz-Expires=86400&X-Amz-Signature=95b19191058842548be8cfca447e2cab96be7eb9a43e9e8796740aaa9108d1ce&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22operations.json%22&x-id=GetObject'

def load_list():
    """загрузка и фильтрация списка операций"""
    req = requests.get(URL_LIST_OPERATIONS)
    data = req.json()
    state = []
    for i in range(len(data)):
        if "state" not in data[i]:
            continue
        else:
            state.append(data[i])
    return state


def definition_operations_executed():
    """Опереляет выполненные (EXECUTED) операции"""
    operations = load_list()
    operations_executed = []
    for i in operations:
        if i['state'] == 'EXECUTED':
            operations_executed.append(i)
    return operations_executed

print(definition_operations_executed())