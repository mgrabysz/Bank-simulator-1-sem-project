from bank_io import (
    info_about_single_client_to_print,
    info_about_loan_to_print,
    info_about_clients_to_print,
    general_info_to_print,
    greeting,
    game_over,
    month_year,
    take_correct_name_from_user,
    take_correct_value_from_user,
    take_correct_rate_from_user,
    take_correct_installments_from_user,
    available
)
from bank_classes import NoBudgetError
import sys


class IncorrectInputError(Exception):
    pass


class Interface():
    def __init__(self, bank):
        self.bank = bank
        self.please = 'Please, choose among available options'

    def simulate(self):
        """
        1. Starts simulation
        2. Prints welcome
        3. Moves to main_menu()
        4. In case of NoBudgetError, stops simulating
        """
        print(greeting())
        try:
            while True:
                self.main_menu()
        except NoBudgetError:
            print(game_over())
            sys.exit()

    def main_menu(self):
        """
        Main menu - display month_year date
        Options from here:
        1. Quit
        2. Display general info
        3. Give a new loan
        4. Move on one month
        5. Move on multiple months
        """
        print('')
        print(month_year(self.bank))
        print('Choose a number of action:')
        print('1. Quit')
        print('2. Display general info')
        print('3. Give a new loan')
        print('4. Move on one month')
        print('5. Move on multiple months')

        input_is_incorrect = True
        while input_is_incorrect:
            action = input('> ')
            if action == '1':
                print('\nThank you for using The Bank Simulator')
                sys.exit()
            elif action == '2' or action == 'info':
                input_is_incorrect = False
                self.display_general_info()
            elif action == '3':
                input_is_incorrect = False
                self.give_a_new_loan()
            elif action == '4':
                input_is_incorrect = False
                self.move_on_one_month()
            elif action == '5':
                input_is_incorrect = False
                self.move_on_multiple_months()
            else:
                print(self.please)

    def display_general_info(self):
        """
        Displays general info about bank
        Options from here:
        1. Back to main menu
        2. Display specific info about client
        """
        general_info = self.bank.general_info()
        display = general_info_to_print(general_info)
        print('')
        print(display)
        print('Choose a number of action:')
        print('1. Back to main menu')
        print('2. Display specific info about client')

        while True:
            action = input('> ')
            if action == '1':
                break
            elif action == '2':
                self.display_client_specific_info()
                break
            else:
                print(self.please)

    def display_client_specific_info(self):
        """
        Displays specific info about client
        Options from here:
        1. Back to main menu
        2. Display specific info about one of the loans
        """
        info_about_clients = self.bank.info_about_clients()
        if not info_about_clients:
            print('There is no one to display info about')
            return

        available_options = []
        for id in info_about_clients:
            available_options.append(id)

        print('Input ID of client you are interested in')
        while True:
            choice = input('> ')
            try:
                id = int(choice)
                client = self.bank.clients_id()[id]
                client_info = self.bank.info_about_single_client(client)
                to_display = info_about_single_client_to_print(client_info)
            except (ValueError, KeyError):
                print(self.please)
                print(available(available_options))
                continue
            break

        print('')
        print(to_display)
        print('Choose a number of action:')
        print('1. Back to main menu')
        print('2. Display specific info about one of the loans')
        while True:
            action = input('> ')
            if action == '1':
                break
            elif action == '2':
                self.display_loan_specific_info(client_info)
                break
            else:
                print(self.please)

    def display_loan_specific_info(self, client_info):
        loans_info = client_info['loans info']
        available_options = []
        for index in loans_info:
            available_options.append(index)
        print('')
        print('Choose a number of loan:')
        while True:
            try:
                choice = input('> ')
                number = int(choice)
                to_display = info_about_loan_to_print(client_info, number)
            except (ValueError, KeyError):
                print(self.please)
                print(available(available_options))
                continue
            break

        print('')
        print('Information about loan:')
        print(to_display)
        print('')

    def give_a_new_loan(self):
        """
        User chooses betweend two options:
        1. Give loan to a new client (is choosen automatically,
            if there are no clients)
        2. Give loan to a client, who already has a loan
        """
        info_about_clients = self.bank.info_about_clients()
        if not info_about_clients:
            print('')
            print("Finally! A client knocks on the door")
            self.new_client_loan()
            return

        print('')
        print('Choose a number of action:')
        print('1. Give loan to a new client (create client)')
        print('2. Give loan to a client who is already our customer')
        while True:
            action = input('> ')
            if action == '1':
                self.new_client_loan()
                break
            elif action == '2':
                self.old_client_loan()
                break
            else:
                print(self.please)
                continue

    def new_client_loan(self):
        """
        1. Takes from user necessary data
        2. Creates new client
        3. Gives a loan to created client
        """
        name = take_correct_name_from_user()
        value = take_correct_value_from_user()
        rate = take_correct_rate_from_user()
        installments = take_correct_installments_from_user(value)
        self.bank.give_loan_to_new_client(
                name,
                value,
                rate,
                installments
            )
        print('')
        print('Action completed succesfully')

    def old_client_loan(self):
        """
        1. Takes from user necessary data
        2. Gives a loan to client who is already a customer
        """
        info_about_clients = self.bank.info_about_clients()
        to_print = info_about_clients_to_print(info_about_clients)
        print('')
        print(to_print)

        available_options = []
        for id in info_about_clients:
            available_options.append(id)

        # Loop used to take correct id from user
        while True:
            print('')
            choice = input('Input ID of client to give another loan: ')
            try:
                id = int(choice)
                if id not in available_options:
                    raise IncorrectInputError
            except (ValueError, IncorrectInputError):
                print(self.please)
                print(available(available_options))
                continue
            break

        value = take_correct_value_from_user()
        rate = take_correct_rate_from_user()
        installments = take_correct_installments_from_user(value)

        self.bank.give_loan_to_bank_client(id, value, rate, installments)

        print('')
        print('Action completed succesfully')

    def move_on_one_month(self):
        """
        Changes month and does all monthly settlements by
        calling method bank.make_monthly_settlement()
        """
        self.bank.make_monthly_settlement()

    def move_on_multiple_months(self):
        """
        1. Takes from user correct number
        2. Moves on desired number of months
        """
        print('')
        print('Enter a number of months to skip:')
        while True:
            number = input('> ')
            try:
                number = int(number)
                if number < 1:
                    raise IncorrectInputError
            except (ValueError, IncorrectInputError):
                print("Number of months has to be a positive integer")
                continue
            break
        for _ in range(number):
            self.bank.make_monthly_settlement()
