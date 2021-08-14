class MultipleUserProfilesWithSameTypeException(Exception):
    pass


class MultipleRecipientsWithSameAccountNumberException(Exception):
    pass


class TransferringMoneyToNonSelfOwnedAccountsException(Exception):
    pass
