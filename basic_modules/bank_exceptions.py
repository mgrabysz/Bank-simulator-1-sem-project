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


class ToBigInstallmentsError(Exception):
    def __init__(self):
        super().__init__("Number of installments is to big for this value")


class NoBudgetError(Exception):
    pass


class YearOutOfRangeError(Exception):
    def __init__(self):
        super().__init__("Even Cyberpunk delay didn't last that long")
