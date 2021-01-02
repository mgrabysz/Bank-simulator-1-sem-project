from bank_classes import Bank
from bank_interface import Interface
from bank_io import load_from_file
import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--load')
    args = parser.parse_args(arguments[1:])

    bank = Bank()

    if args.load:
        path = args.load
        initial_loans = load_from_file(path)
        bank.give_loans_from_initial_data(initial_loans)

    interface = Interface(bank)
    interface.simulate()


if __name__ == "__main__":
    main(sys.argv)
