from bank_classes import (
    Bank,
    Loan,
    Client,
    InvalidValueError,
    InvalidInstallmentsError,
    InvalidRateError,
    InvalidNameError,
    NoBudgetError,
    value_is_correct,
    rate_is_correct,
    installments_is_correct,
)
from decimal import Decimal
from datetime import date
import pytest


def test_create_bank(monkeypatch):

    def get_date_battle_of_grunwald(_):
        return date(1410, 7, 15)
    monkeypatch.setattr(
        Bank,
        'get_first_day_of_month_date',
        get_date_battle_of_grunwald
        )

    bank = Bank()
    assert bank.budget() == Decimal('1000000')
    assert bank.clients_loans() == {}
    assert bank.clients_id() == {}
    assert bank.id_count == 1
    assert bank.current_date == date(1410, 7, 15)


def test_increase_budget_integer():
    bank = Bank()
    bank.increase_budget(250)
    assert bank.budget() == Decimal('1000250')


def test_increase_budget_non_integer():
    bank = Bank()
    bank.increase_budget(20.2)
    assert bank.budget() == Decimal('1000020.20')


def test_increase_budget_and_round():
    bank = Bank()
    bank.increase_budget(20.23778)
    assert bank.budget() == Decimal('1000020.24')


def test_decrease_budget_integer():
    bank = Bank()
    bank.decrease_budget(300)
    assert bank.budget() == Decimal('999700')


def test_decrease_budget_non_integer():
    bank = Bank()
    bank.decrease_budget(300.2)
    assert bank.budget() == Decimal('999699.80')


def test_decrease_budget_and_round():
    bank = Bank()
    bank.decrease_budget(20.3434)
    assert bank.budget() == Decimal('999979.66')


def test_value_is_correct():
    assert value_is_correct(332.46) is True


def test_value_is_correct_negative():
    with pytest.raises(InvalidValueError):
        value_is_correct(-22.9)


def test_value_is_correct_string():
    with pytest.raises(InvalidValueError):
        value_is_correct('Little Mermaid')


def test_rate_is_correct():
    assert rate_is_correct(55.6) is True


def test_rate_is_correct_negative():
    with pytest.raises(InvalidRateError):
        rate_is_correct(-88)


def test_rate_is_correct_greater_than_100():
    with pytest.raises(InvalidRateError):
        rate_is_correct(732.66)


def test_rate_is_correct_string():
    with pytest.raises(InvalidRateError):
        rate_is_correct('Little Mermaid')


def test_installments_is_correct():
    assert installments_is_correct(12) is True


def test_installments_is_correct_non_integer():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct(9.2)


def test_installments_is_correct_negative():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct(-9)


def test_installments_is_correct_string():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct('Little Mermaid')


def test_create_loan():
    loan = Loan(1000, 2, 10)
    assert loan.value() == Decimal(1000)
    assert loan.rate() == Decimal(2)
    assert loan.installments() == 10
    assert loan.payment() == Decimal(102)


def test_create_loan_non_integers():
    loan = Loan(1005.4, 2.2, 12)
    assert loan.value() == Decimal('1005.4')
    assert loan.rate() == Decimal('2.2')
    assert loan.installments() == 12
    assert loan.payment() == Decimal('85.63')


def test_create_client():
    client = Client('Jose Arcadio Morales', 2)
    assert client.name() == 'Jose Arcadio Morales'
    assert client.id() == 2


def test_create_client_with_empty_name():
    with pytest.raises(InvalidNameError):
        Client('', 3)


def test_bank_add_new_client():
    bank = Bank()
    assert bank.clients_id() == {}
    bank.add_new_client('Jose Arcadio Morales')
    client = bank.clients_id()[1]
    assert client.name() == 'Jose Arcadio Morales'
    assert bank.clients_loans()[client] == []


def test_add_new_client_twice():
    bank = Bank()
    bank.add_new_client('Jose Arcadio Morales')
    bank.add_new_client('Emma Watson')
    client = bank.clients_id()[2]
    assert client.name() == 'Emma Watson'
    assert bank.clients_loans()[client] == []


def test_add_new_client_twice_same_name():
    bank = Bank()
    bank.add_new_client('Carlos')
    bank.add_new_client('Carlos')
    first_client = bank.clients_id()[1]
    second_client = bank.clients_id()[2]
    assert first_client.name() == 'Carlos'
    assert first_client.id() == 1
    assert second_client.name() == 'Carlos'
    assert second_client.id() == 2


def test_add_new_client_invalid_name():
    bank = Bank()
    with pytest.raises(InvalidNameError):
        bank.add_new_client('')


def test_give_loan_to_bank_client():
    bank = Bank()
    bank.add_new_client('Jose Arcadio Morales')
    client = bank.clients_id()[1]
    bank.give_loan_to_bank_client(1, 1000, 4, 10)
    loans = bank.clients_loans()[client]
    loan = loans[0]
    assert loan.value() == 1000
    assert loan.rate() == 4
    assert loan.installments() == 10
    assert bank.budget() == Decimal('999000')


def test_give_loan_to_new_client():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    client = bank.clients_id()[1]
    loans = loans = bank.clients_loans()[client]
    loan = loans[0]
    assert client.name() == 'Emma Watson'
    assert loan.value() == 1200
    assert loan.rate() == 3
    assert loan.installments() == 12
    assert bank.budget() == Decimal('998800')


def test_give_two_loans_to_new_client():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_bank_client(1, 500, 2, 4)
    client = bank.clients_id()[1]
    loans = bank.clients_loans()[client]
    first_loan = loans[0]
    second_loan = loans[1]
    assert first_loan.value() == 1200
    assert first_loan.rate() == 3
    assert first_loan.installments() == 12
    assert second_loan.value() == 500
    assert second_loan.rate() == 2
    assert second_loan.installments() == 4
    assert bank.budget() == Decimal('998300')


def test_collect_payment():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    client = bank.clients_id()[1]
    loans = bank.clients_loans()[client]
    loan = loans[0]

    assert bank.budget() == Decimal('998800')
    assert loan.payment() == 103
    assert loan.installments() == 12

    assert bank.collect_payment(loan) is True

    assert bank.budget() == Decimal('998903')
    assert loan.installments() == 11


def test_collect_last_payment():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    client = bank.clients_id()[1]
    loans = bank.clients_loans()[client]
    loan = loans[0]

    for _ in range(11):
        bank.collect_payment(loan)

    assert bank.collect_payment(loan) is False
    assert bank.budget() == Decimal('1000036')


def test_collect_all_payments():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 1)
    emma = bank.clients_id()[1]
    jose = bank.clients_id()[2]
    assert bank.budget() == Decimal('997300')
    bank.collect_all_payments()
    assert bank.budget() == Decimal('998958')
    assert emma in bank.clients_loans()
    assert jose not in bank.clients_loans()
    emma_loans = bank.clients_loans()[emma]
    assert len(emma_loans) == 1


def test_collect_all_payments_multiple_times():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 2)
    bank.give_loan_to_bank_client(1, 300, 1, 3)
    emma = bank.clients_id()[1]
    assert bank.budget() == Decimal('998000')
    assert len(bank.clients_loans()[emma]) == 3

    bank.collect_all_payments()
    assert bank.budget() == Decimal('999599.5')
    assert len(bank.clients_loans()[emma]) == 2

    bank.collect_all_payments()
    assert bank.budget() == Decimal('999963')
    assert len(bank.clients_loans()[emma]) == 1

    bank.collect_all_payments()
    assert bank.budget() == Decimal('1000064')
    assert emma not in bank.clients_loans()

    bank.collect_all_payments()
    assert bank.budget() == Decimal('1000064')


def test_one_month_forward(monkeypatch):

    def get_date_battle_of_grunwald(_):
        return date(1410, 7, 15)
    monkeypatch.setattr(
        Bank,
        'get_first_day_of_month_date',
        get_date_battle_of_grunwald
        )

    bank = Bank()
    assert bank.current_date == date(1410, 7, 15)
    bank.one_month_forward()
    assert bank.current_date == date(1410, 8, 15)


def test_one_month_forward_new_year(monkeypatch):
    def get_date_mickiewicz_birthday(_):
        return date(1798, 12, 24)
    monkeypatch.setattr(
        Bank,
        'get_first_day_of_month_date',
        get_date_mickiewicz_birthday
        )

    bank = Bank()
    assert bank.current_date == date(1798, 12, 24)
    bank.one_month_forward()
    assert bank.current_date == date(1799, 1, 24)


def test_client_debt():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 2)
    bank.give_loan_to_bank_client(1, 300, 1, 3)
    emma = bank.clients_id()[1]
    debt = bank.client_debt(emma)
    assert debt == Decimal('2064')

    bank.collect_all_payments()
    new_debt = bank.client_debt(emma)
    assert new_debt == Decimal('464.50')

    bank.collect_all_payments()
    newest_debt = bank.client_debt(emma)
    assert newest_debt == Decimal('101')


def test_info_about_clients():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 1)
    info = bank.info_about_clients()
    assert info == {
        1: {'name': 'Emma Watson', 'debt': Decimal('1761.00')},
        2: {'name': 'Jose Arcadio Morales', 'debt': Decimal('1030.00')}
    }


def test_info_about_single_client():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_bank_client(1, 500, 5, 2)
    emma = bank.clients_id()[1]
    info = bank.info_about_single_client(emma)

    expected_info = {
        'id': 1,
        'name': 'Emma Watson',
        'total debt': Decimal('1761.00'),
        'loans info': {
            1: {
                'value': 1200,
                'rate': 3,
                'installments': 12,
                'payment': 103,
                'left to pay': 1236
            },
            2: {
                'value': 500,
                'rate': 5,
                'installments': 2,
                'payment': Decimal('262.50'),
                'left to pay': 525
            }
        }
    }
    assert info == expected_info


def test_make_monthly_settlement(monkeypatch):
    def get_date_battle_of_grunwald(_):
        return date(1410, 7, 15)
    monkeypatch.setattr(
        Bank,
        'get_first_day_of_month_date',
        get_date_battle_of_grunwald
        )

    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 1)
    emma = bank.clients_id()[1]
    jose = bank.clients_id()[2]

    assert bank.budget() == Decimal('997300')
    assert bank.current_date == date(1410, 7, 15)

    bank.make_monthly_settlement()

    assert bank.budget() == Decimal('998958')
    assert emma in bank.clients_loans()
    assert jose not in bank.clients_loans()
    emma_loans = bank.clients_loans()[emma]
    assert len(emma_loans) == 1
    assert bank.current_date == date(1410, 8, 15)


def test_expected_income():
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 2)
    expected_income = bank.expected_income()
    assert expected_income == Decimal('1395.5')


def test_general_info(monkeypatch):
    def get_date_battle_of_grunwald(_):
        return date(1410, 7, 15)
    monkeypatch.setattr(
        Bank,
        'get_first_day_of_month_date',
        get_date_battle_of_grunwald
        )
    bank = Bank()
    bank.give_loan_to_new_client('Emma Watson', 1200, 3, 12)
    bank.give_loan_to_new_client('Jose Arcadio Morales', 1000, 3, 1)
    bank.give_loan_to_bank_client(1, 500, 5, 2)
    general_info = bank.general_info()
    expected_info = {
        'budget': Decimal('997300'),
        'date': date(1410, 7, 15),
        'expected income': Decimal('1395.5'),
        'clients info': {
            1: {'name': 'Emma Watson', 'debt': Decimal('1761.00')},
            2: {'name': 'Jose Arcadio Morales', 'debt': Decimal('1030.00')}
        }
    }
    assert general_info == expected_info


def test_no_budget():
    bank = Bank()
    with pytest.raises(NoBudgetError):
        bank.give_loan_to_new_client('Tom Hanks', 1200000, 4, 4)
