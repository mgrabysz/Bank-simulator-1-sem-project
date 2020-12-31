from bank_classes import Bank
from bank_io import (
    info_about_single_client_to_print,
    info_about_loan_to_print,
    general_info_to_print,
    greeting,
    month_year,
    take_correct_name_from_user,
    take_correct_value_from_user,
    take_correct_rate_from_user,
    take_correct_installments_from_user,
)
import sys


class Interface():
    def __init__(self, bank):
        self.bank = bank
        self.please = 'Please, choose among available options'

    def simulate(self):
        """
        1. Starts simulation
        2. Prints welcome
        3. Moves to main_menu()
        """
        print(greeting())
        while True:
            self.main_menu()

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
        print('Choose number of action:')
        print('1. Quit')
        print('2. Display general info')
        print('3. Give a new loan')
        print('4. Move on one month')
        print('5. Move on multiple months')

        input_is_incorrect = True
        while input_is_incorrect:
            action = input('> ')
            if action == '1':
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
        print('')
        print('Choose number of action:')
        print('1. Back to main menu')
        print('2. Display specific info about client')

        while True:
            action = input('> ')
            if action == '1':
                break
            elif action == '2':
                self.display_client_specific_info()
            else:
                print(self.please)

    def display_client_specific_info(self):
        info_about_clients = self.bank.info_about_clients()
        if not info_about_clients:
            print('There are no one to display info about')
            return

        available_options = []
        for id in info_about_clients:
            available_options.append(id)

        print('Input ID of client you are interested in')
        while True:
            choice = input('> ')
            try:
                id = int(choice)
                client = bank.clients_id()[id]
            except (ValueError, KeyError):
                print(self.please)
                print(f'Available options are {available_options}')
                continue

            client_info = bank.info_about_single_client(client)
            to_display = info_about_single_client_to_print(client_info)
            print('')
            print(to_display)
            print('Choose number of action:')
            print('1. Back to main menu')
            print('2. Display specific info about client')
            return

    def give_a_new_loan(self):
        """
        User chooses betweend two options:
        1. Give loan to a new client (create client)
        2. Give loan to a client, who already has a loan
        """
        info_about_clients = self.bank.info_about_clients()
        if not info_about_clients:
            print('')
            print("Finally! A client knocks on the door")
            self.new_client_loan()

    def new_client_loan(self):
        name = take_correct_name_from_user()
        value = take_correct_value_from_user()
        rate = take_correct_rate_from_user()
        installments = take_correct_installments_from_user()
        self.bank.give_loan_to_new_client(
                name,
                value,
                rate,
                installments
            )

    def move_on_one_month(self):
        bank.make_monthly_settlement()


if __name__ == "__main__":
    bank = Bank()
    # bank.give_loan_to_new_client('Magda Grabysz', 1000, 2, 5)
    interface = Interface(bank)
    interface.simulate()
