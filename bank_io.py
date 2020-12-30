# Świadomie zrezygnowałem z testowania niektórych funkcji z tego modułu.
# Zwracają wielolinijkowe stringi, których układ łatwiej jest przejrzeć
# "ocznie", za to poprawność danych jest sprawdzana innymi testami należącymi
# do modułu test_bank_classes

from bank_classes import (
    Bank,
)
# from datetime import date


def clients_info_oneline(id, name, debt):
    line = f'{id:<3}| {name:24}| {debt:<9}\n'
    return line


def info_about_clients_to_print(info):
    to_return = 'ID | NAME' + (' ' * 20) + '| DEBT (zł)\n'
    to_return += (40 * '-') + '\n'
    for id, values in info.items():
        name = values['name']
        debt = values['debt']
        line = clients_info_oneline(id, name, debt)
        to_return += line
    return to_return


def info_about_single_client_to_print(single_client_info):
    id = single_client_info['id']
    name = single_client_info['name']
    total_debt = single_client_info['total debt']
    loans_info = single_client_info['loans info']
    loan_number = len(loans_info)
    to_return = 'Information about client:\n'
    to_return += f'ID: {id}\n'
    to_return += f'NAME: {name}\n'
    to_return += f'TOTAL DEBT: {total_debt} zł\n'
    to_return += f'NUMBER OF CURRENT LOANS: {loan_number}\n'
    for index, loan in loans_info.items():
        pay = loan['left to pay']
        num = loan['installments']
        inst = 'installment' if num == 1 else 'installments'
        to_return += f'{index}. {pay} zł left to pay in {num} {inst}\n'
    return to_return


def info_about_loan_to_print(single_client_info, number):
    name = single_client_info['name']
    loans_info = single_client_info['loans info']
    loan = loans_info[number]
    value = loan['value']
    rate = loan['rate']
    installments = loan['installments']
    payment = loan['payment']
    to_pay = loan['left to pay']

    to_return = f'OWNER: {name}\n'
    to_return += f'TOTAL VALUE: {value} zł\n'
    to_return += f'RATE: {rate} %\n'
    to_return += f'INSTALMENTS LEFT: {installments}\n'
    to_return += f'SINGLE INSTALLMENT VALUE: {payment} zł\n'
    to_return += f'VALUE LEFT TO PAY: {to_pay} zł\n'
    return to_return


def general_info_to_print(general_info):
    budget = general_info['budget']
    cur_date = general_info['date']
    period = cur_date.strftime("%B %Y")
    expected_income = general_info['expected income']
    clients_info = general_info['clients info']
    to_return = f'SETTLEMENT PERIOD: {period}\n'
    to_return += f'BUDGET: {budget} zł\n'
    to_return += f'EXPECTED INCOME: {expected_income} zł\n'
    to_return += 'INFO ABOUT CLIENTS:\n'
    clients = info_about_clients_to_print(clients_info)
    to_return += clients
    return to_return


bank = Bank()
bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
bank.give_loan_to_bank_client(1, 500, 5, 1)

general_info = bank.general_info()
to_print = general_info_to_print(general_info)
print(to_print)
