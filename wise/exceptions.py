from global_common import CustomException


class MultipleUserProfilesWithSameTypeException(CustomException):
    pass


class MultipleRecipientsWithSameAccountNumberException(CustomException):
    pass


class TransferringMoneyToNonSelfOwnedAccountsException(CustomException):
    pass


class ReserveAccountNotFound(CustomException):
    pass
