from basic_modules.bank_exceptions import (
    InvalidValueError,
    InvalidRateError,
    InvalidInstallmentsError,
    ToBigInstallmentsError
)
from basic_modules.bank_checking_functions import (
    value_is_correct,
    rate_is_correct,
    installments_is_correct,
)
import pytest


def test_value_is_correct():
    assert value_is_correct(332.46) is True


def test_value_is_correct_negative():
    with pytest.raises(InvalidValueError):
        value_is_correct(-22.9)


def test_value_is_correct_string():
    with pytest.raises(InvalidValueError):
        value_is_correct('Little Mermaid')


def test_value_is_correct_lesser_than_100():
    with pytest.raises(InvalidValueError):
        value_is_correct(66)


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
    assert installments_is_correct(12, 10000) is True


def test_installments_is_correct_non_integer():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct(9.2, 10000)


def test_installments_is_correct_negative():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct(-9, 10000)


def test_installments_is_correct_string():
    with pytest.raises(InvalidInstallmentsError):
        installments_is_correct('Little Mermaid', 10000)


def test_installments_is_correct_to_bit():
    with pytest.raises(ToBigInstallmentsError):
        installments_is_correct(2048, 100)
