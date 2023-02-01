from utils import *

def test_print_operation():
    assert print_operation(0) == '08.12.2019 Открытие вклада\n ->  Счет **5907\n41096.24 USD\n'
    assert print_operation(1) == '07.12.2019 Перевод организации\nVisa Classic 2842 84** **** 9012 ->  Счет **3655\n48150.39 USD\n'
    assert print_operation(2) == '19.11.2019 Перевод организации\nMaestro 7810 46** **** 5568 ->  Счет **2869\n30153.72 руб.\n'