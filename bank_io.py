# Świadomie zrezygnowałem z testowania większości funkcji z tego modułu.
# Zwracają wielolinijkowe stringi, których układ łatwiej jest przejrzeć
# "ocznie", za to poprawność danych jest sprawdzana innymi testami należącymi
# do modułu test_bank_classes

from bank_classes import (
    value_is_correct,
    rate_is_correct,
    installments_is_correct,
    name_is_correct,
    InvalidValueError,
    InvalidRateError,
    InvalidInstallmentsError,
    InvalidNameError,
)
import csv


class MalformedDataError(Exception):
    pass


def clients_info_oneline(id, name, debt):
    """
    Returns one line string with info about client
    """
    line = f'{id:<3}| {name:24}| {debt:<9}\n'
    return line


def info_about_clients_to_print(info_about_clients):
    """
    Returns info about all clients as multi-line, user-friendly string
    """
    if info_about_clients:
        to_return = 'ID | NAME' + (' ' * 20) + '| DEBT (PLN)\n'
        to_return += (40 * '-') + '\n'
        for id, values in info_about_clients.items():
            name = values['name']
            debt = values['debt']
            line = clients_info_oneline(id, name, debt)
            to_return += line
        return to_return
    else:
        to_return = "You do not have any client this month"
        return to_return


def info_about_single_client_to_print(single_client_info):
    """
    Returns info about single client as multi-line, user-friendly string
    """
    id = single_client_info['id']
    name = single_client_info['name']
    total_debt = single_client_info['total debt']
    loans_info = single_client_info['loans info']
    loan_number = len(loans_info)
    to_return = 'Information about client:\n'
    to_return += f'ID: {id}\n'
    to_return += f'NAME: {name}\n'
    to_return += f'TOTAL DEBT: {total_debt} PLN\n'
    to_return += f'NUMBER OF CURRENT LOANS: {loan_number}\n'
    for index, loan in loans_info.items():
        pay = loan['left to pay']
        num = loan['installments']
        inst = 'installment' if num == 1 else 'installments'
        to_return += f'{index}. {pay} PLN left to pay in {num} {inst}\n'
    return to_return


def info_about_loan_to_print(single_client_info, number):
    """
    Returns info about single loan as multi-line, user-friendly string
    """
    name = single_client_info['name']
    loans_info = single_client_info['loans info']
    loan = loans_info[number]
    value = loan['value']
    rate = loan['rate']
    installments = loan['installments']
    payment = loan['payment']
    to_pay = loan['left to pay']

    to_return = f'OWNER: {name}\n'
    to_return += f'TOTAL VALUE: {value} PLN\n'
    to_return += f'RATE: {rate} %\n'
    to_return += f'INSTALMENTS LEFT: {installments}\n'
    to_return += f'SINGLE INSTALLMENT VALUE: {payment} PLN\n'
    to_return += f'VALUE LEFT TO PAY: {to_pay} PLN'
    return to_return


def general_info_to_print(general_info):
    """
    Returns general info as multi-line, user-friendly string
    """
    budget = general_info['budget']
    cur_date = general_info['date']
    period = cur_date.strftime("%B %Y")
    expected_income = general_info['expected income']
    clients_info = general_info['clients info']
    to_return = f'SETTLEMENT PERIOD: {period}\n'
    to_return += f'BUDGET: {budget} PLN\n'
    to_return += f'EXPECTED INCOME: {expected_income} PLN\n'
    to_return += 'INFO ABOUT CLIENTS:\n'
    clients = info_about_clients_to_print(clients_info)
    to_return += clients
    return to_return


def greeting():
    """
    Returns greeting text
    """
    greeting = 'Welcome to The Bank Simulator!\n\n'
    greeting += 'You just have inherited The Goodbank Company - '
    greeting += 'a bank established by your beloved father,\n'
    greeting += 'who with his titanic work managed to gather budget of '
    greeting += '1,000,000 PLN\n\n'
    greeting += 'You can now add new clients and give them loans.\n\n'
    greeting += "The future of your father's legacy is in your hands!"
    return greeting


def game_over():
    """
    Returns text informing about bankruptcy
    """
    game_over = '\nYour careless politics has led to total bankruptcy... '
    game_over += 'Your father must be spinning in his grave!\n'
    game_over += 'Thank you for using The Bank Simulator'
    return game_over


def month_year(bank):
    """
    Returns date in format 'April 1999'
    """
    my_date = bank.current_date
    month_year = my_date.strftime("%B %Y")
    return month_year


def take_correct_name_from_user():
    """
    Asks user for entering client name until input is correct
    """
    while True:
        try:
            name = input("Enter client's name: ")
            if name_is_correct(name):
                return name
        except InvalidNameError:
            print('Name cannot be empty')
            continue


def take_correct_value_from_user():
    """
    Asks user for entering loan value until input is correct
    """
    while True:
        try:
            value = input("Enter total value of the loan: ")
            if value_is_correct(value):
                return value
        except InvalidValueError:
            print('Value has to be positive number')
            continue


def take_correct_rate_from_user():
    """
    Asks user for entering loan rate until input is correct
    """
    while True:
        try:
            rate = input("Enter rate (e.g. '2' means 2% rate): ")
            if rate_is_correct(rate):
                return rate
        except InvalidRateError:
            print('Rate has to be a number from range [0, 100]')
            continue


def take_correct_installments_from_user():
    """
    Asks user for entering number of installments until input is correct
    """
    while True:
        try:
            installments = input("Enter number of monthly installments: ")
            if installments_is_correct(installments):
                return installments
        except InvalidInstallmentsError:
            print('Number of installments has to be a positive integer')
            continue


def read_from_csv(file_handle):
    """
    Reads data from csv file handle and returs a list of dictionaries
    """
    initial_loans = []
    reader = csv.DictReader(file_handle)
    try:
        for row in reader:
            initial_loan = {}
            name = None if row['name'] == '[previous]' else row['name']
            value = row['value']
            rate = row['rate']
            installments = row['installments']
            new_or_not = False if row['name'] == '[previous]' else True
            initial_loan['new or not'] = new_or_not

            # Checking if data is correct
            value_is_correct(value)
            rate_is_correct(rate)
            installments_is_correct(installments)
            if initial_loan['new or not'] is True:
                name_is_correct(name)

            initial_loan['name'] = name
            initial_loan['value'] = value
            initial_loan['rate'] = rate
            initial_loan['installments'] = installments
            initial_loans.append(initial_loan)
    except (csv.Error, KeyError) as e:
        raise MalformedDataError(str(e))
    return initial_loans


def load_from_file(path):
    """
    Loads data from file
    """
    with open(path, 'r') as file_handle:
        initial_loans = read_from_csv(file_handle)
    return initial_loans
