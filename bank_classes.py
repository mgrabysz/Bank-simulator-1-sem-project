from decimal import Decimal
from datetime import date


class InvalidValueError(Exception):
    def __init__(self):
        super().__init__("Invalid value detected")


class InvalidRateError(Exception):
    def __init__(self):
        super().__init__("Invalid rate detected")


class InvalidInstallmentsError(Exception):
    def __init__(self):
        super().__init__("Invalid installments number detected")


class InvalidNameError(Exception):
    def __init__(self):
        super().__init__("Name cannot be empty")


class NoBudgetError(Exception):
    pass


def value_is_correct(value):
    """
    Returns True if given value is a positive number
    """
    try:
        value = float(value)
        if value > 0:
            return True
        else:
            raise InvalidValueError
    except ValueError:
        raise InvalidValueError


def rate_is_correct(rate):
    """
    Returns True if given rate is a number from range [0, 100]
    """
    try:
        rate = float(rate)
        if rate < 0 or rate > 100:
            raise InvalidRateError
        else:
            return True
    except ValueError:
        raise InvalidRateError


def installments_is_correct(installments):
    """
    Returns True if given installments is positive integer
    """
    if type(installments) is str:
        try:
            installments = int(installments)
        except ValueError:
            raise InvalidInstallmentsError
    elif type(installments) is not int:
        raise InvalidInstallmentsError

    if installments < 1:
        raise InvalidInstallmentsError
    return True


def name_is_correct(name):
    if not name:
        raise InvalidNameError
    else:
        return True


def get_first_day_of_month_date():
    my_date = date.today()
    first_day = my_date.replace(day=1)
    return first_day


class Bank():
    """
    Class Bank. Contains attributes:
    :param budget: bank's total budget
    :type budget: Decimal

    :param clients_loans: dictionary mapping client to his loans
    :type clients_loans: dict

    :param clients_id: dictionary mapping unique ID to client
    :type clients_id: dict

    :param id_count: this param increases by 1 with every created client
        to provide uniqueness of ID
    :type id_count: int

    :param current_date: represents current date in the bank simulator
    :type current_date: datetime.date
    """
    def __init__(self, budget=Decimal(1000000)):
        self._budget = budget
        self._clients_loans = {}
        self._clients_id = {}
        self.id_count = 1
        self.current_date = get_first_day_of_month_date()

    def budget(self):
        return self._budget

    def increase_budget(self, value):
        """
        1. Increases budget by given value
        2. Rounds budget to have monetary format
        """
        value = str(value)
        self._budget += Decimal(value)
        var = self._budget
        self._budget = self._budget.quantize(Decimal('.01'))
        var.quantize(Decimal('.01'))

    def decrease_budget(self, value):
        """
        1. Decreases budget by given value
        2. Rounds budget to have monetary format
        """
        value = str(value)
        self._budget -= Decimal(value)
        self._budget = self._budget.quantize(Decimal('.01'))
        if self.budget() <= 0:
            raise NoBudgetError

    def clients_loans(self):
        return self._clients_loans

    def clients_id(self):
        return self._clients_id

    def add_new_client(self, client_name):
        """
        1. Creates unique id for client
        2. Appends new elements to clients_id and clients_loans
        3. Increases id_count by 1
        """
        id = self.id_count
        client = Client(client_name, id)
        self._clients_id[id] = client
        self._clients_loans[client] = []
        self.id_count += 1
        return id

    def give_loan_to_bank_client(self, client_id, value, rate, installments):
        """
        1. Creates new loan assigned to a client, who already has a loan.
        2. Decreases bank budget by loan value
        """
        client = self.clients_id()[client_id]
        loan = Loan(value, rate, installments)
        self._clients_loans[client].append(loan)
        self.decrease_budget(value)

    def give_loan_to_new_client(self, client_name, value, rate, installments):
        """
        1. Creates new client and then creates new loan assigned to this client
        2. Decreases bank budet by loan value
        """
        client_id = self.add_new_client(client_name)
        self.give_loan_to_bank_client(client_id, value, rate, installments)

    def collect_payment(self, loan):
        """
        1. Increases bank budget by single payment
        2. Decreases loan.installments by 1
        3. Increases loan.inst_paid by 1
        4. If loan.installments == 0, returns False. Otherwise returns True
        """
        payment = loan.payment()
        self.increase_budget(payment)
        loan.decrease_installments_by_one()
        loan.increase_inst_paid_by_one()
        to_return = False if loan.installments() == 0 else True
        return to_return

    def collect_all_payments(self):
        """
        1. Iterates over clients_loans dictionary
        2. Collect payments from every loan of every client
        3. If function collect_payment returns False, discards loan
        4. If client's only loan is discarded, discard client
        """
        clients_to_discard = []
        for client, loan_list in self.clients_loans().items():
            loans_to_discard = []
            for loan in loan_list:
                loan_is_valid = self.collect_payment(loan)
                if not loan_is_valid:
                    loans_to_discard.append(loan)
            for loan in loans_to_discard:
                loan_list.remove(loan)
            if not loan_list:
                clients_to_discard.append(client)

    # This bizarre construct is meant to prevent removing
    # list/dict element during iteration over that list/dict

        for client in clients_to_discard:
            del self._clients_loans[client]

    def one_month_forward(self):
        """
        Changes current_date to one month forward
        """
        cur_date = self.current_date
        if cur_date.month == 12:
            forward = cur_date.replace(month=1, year=cur_date.year+1)
        else:
            forward = cur_date.replace(month=cur_date.month+1)
        self.current_date = forward

    def make_monthly_settlement(self):
        """
        1. Collects money from all clients
        2. Changes date to next month
        """
        self.collect_all_payments()
        self.one_month_forward()

    def client_debt(self, client):
        """
        Calcultes how much a client owes to the bank
        """
        debt = Decimal(0)
        loans = self.clients_loans()[client]
        for loan in loans:
            value = loan.value()
            rate = loan.rate()
            inst_paid = loan.inst_paid()
            norm_payment = loan.norm_payment()
            total_value_to_pay = ((rate + 100) * value / 100)
            total_value_to_pay = total_value_to_pay.quantize(Decimal('.01'))
            to_pay = total_value_to_pay - (inst_paid * norm_payment)
            debt += to_pay
        return debt

    def info_about_clients(self):
        """
        Returns dictionary according to scheme:
        {client_id: {name: name, debt: debt}}
        """
        info_about_clients = {}
        for client in self.clients_loans():
            name = client.name()
            id = client.id()
            debt = self.client_debt(client)
            name_debt = {"name": name, "debt": debt}
            info_about_clients[id] = name_debt
        return info_about_clients

    def info_about_single_client(self, client):
        """
        Returns a dictionary with info about client according to scheme:
        {
            id: id,
            name: name,
            total debt: debt
            loans info: {
                1: {value: a, rate: b, installments: c, payment: d, to pay: e}
                2: {value: a, rate: b, installments: c, payment: d, to pay: e}
                    }
         }
        """
        id = client.id()
        name = client.name()
        total_debt = self.client_debt(client)
        single_client_info = {
            "id": id,
            "name": name,
            "total debt": total_debt,
            "loans info": {}
        }
        loans = self.clients_loans()[client]
        for index, loan in enumerate(loans):
            value = loan.value()
            rate = loan.rate()
            installments = loan.installments()
            payment = loan.payment()
            norm_payment = loan.norm_payment()
            inst_paid = loan.inst_paid()
            total_value_to_pay = ((rate + 100) * value / 100)
            total_value_to_pay = total_value_to_pay.quantize(Decimal('.01'))
            to_pay = total_value_to_pay - (inst_paid * norm_payment)

            loan_info = {
                'value': value,
                'rate': rate,
                'installments': installments,
                'payment': payment,
                'left to pay': to_pay
            }
            single_client_info["loans info"][index + 1] = loan_info
        return single_client_info

    def expected_income(self):
        """
        Returns expected income after current settlement period
        """
        clients_loans = self.clients_loans()
        expected_income = Decimal(0)
        for client, loans in clients_loans.items():
            for loan in loans:
                expected_income += loan.payment()
        return expected_income

    def general_info(self):
        """
        Returns dictionary according to scheme: {
            'budget': self.budget(),
            'date': self.current_date,
            'expected income': self.expected_income()
            'clients info': info_about_clients()
        }
        """
        budget = self.budget()
        current_date = self.current_date
        expected_income = self.expected_income()
        clients_info = self.info_about_clients()
        general_info = {
            'budget': budget,
            'date': current_date,
            'expected income': expected_income,
            'clients info': clients_info
        }
        return general_info

    def give_loans_from_initial_data(self, initial_loans):
        """
        This method is used when starting simulator with some initial data from
        external file.
        """
        for initial_loan in initial_loans:
            name = initial_loan['name']
            value = initial_loan['value']
            rate = initial_loan['rate']
            installments = initial_loan['installments']
            if initial_loan['new or not'] is True:
                self.give_loan_to_new_client(name, value, rate, installments)
            else:
                id = self.id_count - 1
                self.give_loan_to_bank_client(id, value, rate, installments)


class Loan():
    """
    Class Loan. Contains attributes:

    :param value: total value of a loan
    :type value: Decimal

    :param rate: rate of interest
    :type rate: Decimal

    :param installments: number of installments left
    :type installments: int

    :param norm_payment: value of single payment
    :type norm_payment: Decimal

    :param inst_paid: number of installments paid
    :type inst_paid: int
    """
    def __init__(self,
                 value,
                 rate,
                 installments,
                 ):

        if value_is_correct(value):
            self._value = Decimal(str(value))

        if rate_is_correct(rate):
            self._rate = Decimal(str(rate))

        if installments_is_correct(installments):
            self._installments = int(installments)

        self._norm_payment = self.calculate_payment()
        self._inst_paid = 0

    def calculate_payment(self):
        """
        Calculates value of a single installment.
        """
        rate = self.rate()
        value = self.value()
        installments = self.installments()

        norm_payment = (((rate + 100) * value / 100) / installments)
        return norm_payment.quantize(Decimal('.01'))

    def calculate_last_payment(self):
        """
        Calculates value of last payment.
        Last payment is greater or equal to previous payments
        to make up for rounding innacuracy.
        """
        value = self.value()
        rate = self.rate()
        inst_paid = self.inst_paid()
        norm_payment = self.norm_payment()
        total_value_to_pay = ((rate + 100) * value / 100)
        total_value_to_pay = total_value_to_pay.quantize(Decimal('.01'))
        to_pay = total_value_to_pay - (inst_paid * norm_payment)
        return to_pay

    def value(self):
        return self._value

    def rate(self):
        return self._rate

    def installments(self):
        return self._installments

    def set_installments(self, new_installments):
        self._installments = new_installments

    def decrease_installments_by_one(self):
        self._installments -= 1

    def increase_inst_paid_by_one(self):
        self._inst_paid += 1

    def norm_payment(self):
        return self._norm_payment

    def payment(self):
        if self.installments() == 1:
            return self.calculate_last_payment()
        else:
            return self.norm_payment()

    def inst_paid(self):
        return self._inst_paid


class Client():
    """
    :param name: client's name
    :type name: str

    :param id: client's unique ID
    :type id: int
    """
    def __init__(self, name, id):
        if name_is_correct(name):
            self._name = str(name)
        self._id = id

    def name(self):
        return self._name

    def id(self):
        return self._id
