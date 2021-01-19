from basic_modules.bank_io import (
    read_from_csv,
    MalformedDataError,
)
from basic_modules.bank_classes import (
    InvalidRateError,
    InvalidNameError,
)
from io import StringIO
import pytest


def test_read_from_csv():
    data = 'name,value,rate,installments\n'
    data += 'Michael Scott,1200,4.5,10\n'
    data += '[previous],800,2,5'
    file_handle = StringIO(data)
    initial_loans = read_from_csv(file_handle)

    expected_info = [
        {
            'name': 'Michael Scott',
            'new or not': True,
            'value': '1200',
            'rate': '4.5',
            'installments': '10'
        },
        {
            'name': None,
            'new or not': False,
            'value': '800',
            'rate': '2',
            'installments': '5'
        }
    ]
    assert initial_loans == expected_info


def test_read_from_csv_rate_error():
    data = 'name,value,rate,installments\n'
    data += 'Michael Scott,1200,,10\n'
    data += '[previous],800,2,5'
    file_handle = StringIO(data)
    with pytest.raises(InvalidRateError):
        read_from_csv(file_handle)


def test_read_from_csv_name_error():
    data = 'name,value,rate,installments\n'
    data += ',1200,4.5,10\n'
    data += '[previous],800,2,5'
    file_handle = StringIO(data)
    with pytest.raises(InvalidNameError):
        read_from_csv(file_handle)


def test_read_from_csv_malformed_data():
    data = 'name,value,,installments\n'
    data += 'Michael Scott,1200,4.5,10\n'
    data += '[previous],800,2,5'
    file_handle = StringIO(data)
    with pytest.raises(MalformedDataError):
        read_from_csv(file_handle)
