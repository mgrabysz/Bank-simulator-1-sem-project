from basic_modules.bank_classes import (
    Bank,
    InvalidNameError,
    InvalidValueError,
    InvalidRateError,
    InvalidInstallmentsError,
    ToBigInstallmentsError
)
from basic_modules.bank_interface import Interface
from basic_modules.bank_io import load_from_file, MalformedDataError
import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--load')
    args = parser.parse_args(arguments[1:])

    bank = Bank()

    if args.load:
        try:
            path = args.load
            initial_loans = load_from_file(path)
            bank.give_loans_from_initial_data(initial_loans)
        except (
            InvalidNameError,
            InvalidValueError,
            InvalidRateError,
            InvalidInstallmentsError,
            MalformedDataError,
            ToBigInstallmentsError
        ) as e:
            print(e)
            print(f'File {path} contains invalid data')
            sys.exit()

    interface = Interface(bank)
    interface.simulate()


if __name__ == "__main__":
    main(sys.argv)
