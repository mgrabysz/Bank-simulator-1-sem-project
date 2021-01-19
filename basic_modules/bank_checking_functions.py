from decimal import Decimal
from basic_modules.bank_exceptions import (
    InvalidValueError,
    InvalidRateError,
    InvalidInstallmentsError,
    InvalidNameError,
    ToBigInstallmentsError,
)


def value_is_correct(value):
    """
    Returns True if given value is a number equal or greater than 100
    """
    try:
        value = float(value)
        if value >= 100:
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


def installments_is_correct(installments, value):
    """
    Returns True if given installments is positive integer not too big for
    given value
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

    value = Decimal(value)
    # value always is tested before installments, so is correct
    if ((installments ** 2) > (200 * value)):
        raise ToBigInstallmentsError

    return True


def name_is_correct(name):
    if not name:
        raise InvalidNameError
    else:
        return True
