'''импорты и переменные(константы)'''
import requests, json, os
from datetime import datetime

URL_LIST_OPERATIONS = 'https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230201%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230201T112404Z&X-Amz-Expires=86400&X-Amz-Signature=85f20d35a166ca833b589f87bcbf03054c08df9df6c0e934078920f8b6b05683&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22operations.json%22&x-id=GetObject'

def load_list():
    """загрузка и фильтрация списка операций по 'state'"""
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


def sort_date_operations():
    """форматирует дату оперций"""
    operatio = definition_operations_executed()
    for i in operatio:
        date = i['date']
        thedate = datetime.fromisoformat(date)
        date_formatted = thedate.strftime('%Y-%m-%d %H:%M:%S')
        i['date'] = date_formatted
    return operatio


def date_sort_operation():
    """сортирует по дате оперций"""
    list = sort_date_operations()
    list.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    return list


def print_last5_operation():
    """выводит 5 последних опреаций"""
    operat = date_sort_operation()
    opera = []
    for i in range(5):
      opera.append(operat[i])
    return opera


def print_operation(numb):
    """выводит форматированное сообщение по индексу"""
    oper = print_last5_operation()
    date = oper[numb]['date']
    thedate = datetime.fromisoformat(date)
    date_format = thedate.strftime('%d.%m.%Y')
    description = oper[numb]['description']
    if 'from' in oper[numb]:
        from1 = oper[numb]['from']
        if 'Maestro' in from1:
            from1 = f'{from1[0:12]} {from1[13:15]}** **** {from1[-4:len(from1)]}'
        elif 'Visa'  in from1:
            from1 = f'{from1[0:17]} {from1[14:16]}** **** {from1[-4:len(from1)]}'
        elif 'Счет'  in from1:
            from1 = f'{from1[0:9]} {from1[9:11]}** **** {from1[-4:len(from1)]}'
    else:
        from1 = ''
    to0 = oper[numb]['to']
    to1 = f' Счет **{to0[-4:len(to0)]}'
    summa = oper[numb]['operationAmount']['amount']
    currency = oper[numb]['operationAmount']['currency']['name']
    message = f'{date_format} {description}\n{from1} -> {to1}\n{summa} {currency}\n'
    return message