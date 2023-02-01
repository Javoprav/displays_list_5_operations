"""Импорты и переменные(константы)"""
from datetime import datetime

import requests

URL_LIST_OPERATIONS = 'https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d22c7143-d55e-4f1d-aa98' \
                      '-e9b15e5e5efc/operations.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED' \
                      '-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230201%2Fus-west-2%2Fs3%2Faws4_request&X' \
                      '-Amz-Date=20230201T112404Z&X-Amz-Expires=86400&X-Amz-Signature' \
                      '=85f20d35a166ca833b589f87bcbf03054c08df9df6c0e934078920f8b6b05683&X-Amz-SignedHeaders=host' \
                      '&response-content-disposition=filename%3D%22operations.json%22&x-id=GetObject'


def load_list_state():
    """Загрузка и фильтрация списка операций по 'state'"""
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
    """Определяет выполненные (EXECUTED) операции"""
    operations = load_list_state()
    operations_executed = []
    for i in operations:
        if i['state'] == 'EXECUTED':
            operations_executed.append(i)
    return operations_executed


def sort_date_operations():
    """Форматирует дату операций"""
    date_operations = definition_operations_executed()
    for i in date_operations:
        date = i['date']
        the_date = datetime.fromisoformat(date)
        date_formatted = the_date.strftime('%Y-%m-%d %H:%M:%S')
        i['date'] = date_formatted
    return date_operations


def date_sort_operation():
    """Сортирует по дате операций"""
    list_sort = sort_date_operations()
    list_sort.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    return list_sort


def print_last5_operation():
    """Выводит 5 последних операций"""
    last5_operation = date_sort_operation()
    operation_5 = []
    for i in range(5):
        operation_5.append(last5_operation[i])
    return operation_5


def print_operation(numb):
    """Выводит форматированное сообщение по индексу"""
    operation_numb = print_last5_operation()
    date = operation_numb[numb]['date']
    the_date = datetime.fromisoformat(date)
    date_format = the_date.strftime('%d.%m.%Y')
    description = operation_numb[numb]['description']
    if 'from' in operation_numb[numb]:
        from1 = operation_numb[numb]['from']
        if 'Maestro' in from1:
            from1 = f'{from1[0:12]} {from1[13:15]}** **** {from1[-4:len(from1)]}'
        elif 'Visa' in from1:
            from1 = f'{from1[0:17]} {from1[14:16]}** **** {from1[-4:len(from1)]}'
        elif 'Счет' in from1:
            from1 = f'{from1[0:9]} {from1[9:11]}** **** {from1[-4:len(from1)]}'
    else:
        from1 = ''
    to0 = operation_numb[numb]["to"]
    to1 = f' Счет **{to0[-4:len(to0)]}'
    summa = operation_numb[numb]["operationAmount"]['amount']
    currency = operation_numb[numb]['operationAmount']['currency']['name']
    message_text = f'{date_format} {description}\n{from1} -> {to1}\n{summa} {currency}\n'
    return message_text
