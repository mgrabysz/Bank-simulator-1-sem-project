from bank_classes import Bank
from bank_interface import Interface

if __name__ == "__main__":
    bank = Bank()
    interface = Interface(bank)
    interface.simulate()
