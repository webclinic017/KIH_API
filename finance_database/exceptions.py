from global_common import CustomException


class DataNotFoundException(CustomException):
    pass


class ExcelFileOpenedByAnotherApplication(CustomException):
    pass


class BalanceForCurrencyNotFoundException(CustomException):
    pass


class InsufficientFundsException(CustomException):
    pass
