import enum
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

import global_common
import wise_models
from wise.exceptions import MultipleUserProfilesWithSameTypeException, MultipleRecipientsWithSameAccountNumber


class ProfileTypes(enum.Enum):
    PERSONAL: str = "personal"
    BUSINESS: str = "business"


@dataclass
class UserProfile:
    id: int
    type: ProfileTypes
    first_name: str
    last_name: str
    date_of_birth: str

    @classmethod
    def get_all(cls) -> List["UserProfile"]:
        user_profiles_list: List[UserProfile] = []

        for wise_user_profile in wise_models.UserProfiles.call():
            user_profiles_list.append(UserProfile(wise_user_profile.id, global_common.get_enum_from_value(wise_user_profile.type, ProfileTypes), wise_user_profile.details.firstName, wise_user_profile.details.lastName, wise_user_profile.details.dateOfBirth))

        return user_profiles_list

    @classmethod
    def get_by_profile_type(cls, profile_type: ProfileTypes) -> "UserProfile":
        return_user_profile: UserProfile = None

        for user_profile in UserProfile.get_all():
            if user_profile.type == profile_type:
                if return_user_profile is None:
                    return_user_profile = user_profile
                else:
                    raise MultipleUserProfilesWithSameTypeException()
        return return_user_profile


@dataclass
class AccountBalance:
    currency: global_common.Currency
    balance: Decimal
    reserved_amount: Decimal

    def __init__(self, wise_balance: wise_models.Balance):
        self.currency = global_common.get_enum_from_value(wise_balance.currency, global_common.Currency)
        self.balance = Decimal(str(wise_balance.amount.value))
        self.reserved_amount = Decimal(str(wise_balance.reservedAmount.value))


@dataclass
class Account:
    id: int
    profile_id: int
    recipient_id: int
    is_active: bool
    balances_list: List[AccountBalance]

    def __init__(self, wise_account: wise_models.Account):
        self.id = wise_account.id
        self.profile_id = wise_account.profileId
        self.recipient_id = wise_account.recipientId
        self.is_active = wise_account.active

        self.balances_list = []
        for wise_balance in wise_account.balances:
            self.balances_list.append(AccountBalance(wise_balance))

    @classmethod
    def get_by_profile_type(cls, profile_type: ProfileTypes) -> List["Account"]:
        user_profile: UserProfile = UserProfile.get_by_profile_type(profile_type)
        accounts_list: List[Account] = []

        for wise_account in wise_models.Account.call(user_profile.id):
            accounts_list.append(Account(wise_account))

        return accounts_list


@dataclass
class ExchangeRate:
    exchange_rate: Decimal
    from_currency: global_common.Currency
    to_currency: global_common.Currency

    @classmethod
    def get(cls, from_currency: global_common.Currency, to_currency: global_common.Currency) -> "ExchangeRate":
        wise_exchange_rate: wise_models.ExchangeRate = wise_models.ExchangeRate.call(from_currency.value, to_currency.value)
        return ExchangeRate(Decimal(str(wise_exchange_rate.rate)), from_currency, to_currency)


@dataclass
class Recipient:
    account_id: int
    profile_id: int
    name: str
    currency: global_common.Currency
    is_active: bool
    is_self_owned: bool
    account_number: str
    swift_code: str
    bank_name: str
    branch_name: str
    iban: str
    bic: str

    @classmethod
    def get_all_by_profile_type(cls, profile_type: ProfileTypes) -> List["Recipient"]:
        user_profile: UserProfile = UserProfile.get_by_profile_type(profile_type)
        recipient_list: List[Recipient] = []

        for wise_recipient in wise_models.Recipient.call(user_profile.id):
            recipient_list.append(Recipient(wise_recipient.id, wise_recipient.profile, wise_recipient.accountHolderName, global_common.get_enum_from_value(wise_recipient.currency, global_common.Currency), wise_recipient.active, wise_recipient.ownedByCustomer, wise_recipient.details.accountNumber, wise_recipient.details.swiftCode, wise_recipient.details.bankName, wise_recipient.details.branchName, wise_recipient.details.swiftCode, wise_recipient.details.bic))

        return recipient_list

    @classmethod
    def get_by_account_number_and_profile_type(cls, account_number: str, profile_type: ProfileTypes) -> "Recipient":
        return_recipient: Recipient = None
        for recipient in Recipient.get_all_by_profile_type(profile_type):
            if recipient.account_number == account_number:
                if return_recipient is None:
                    return_recipient = recipient
                else:
                    raise MultipleRecipientsWithSameAccountNumber()

        return return_recipient


@dataclass
class Transfer:
    profile_id: int
    from_currency: global_common.Currency
    to_currency: global_common.Currency
    from_amount: Decimal
    to_amount: Decimal
    recipient: Recipient
    exchange_rate: ExchangeRate
    is_successful: bool
    error_message: Optional[str]
    error_code: Optional[str]

    def __init__(self, user_profile: UserProfile, recipient: Recipient, wise_transfer: wise_models.Transfer, wise_fund: wise_models.Fund):
        self.profile_id = user_profile.id
        self.from_currency = global_common.get_enum_from_value(wise_transfer.sourceCurrency, global_common.Currency)
        self.to_currency = global_common.get_enum_from_value(wise_transfer.targetCurrency, global_common.Currency)
        self.from_amount = Decimal(str(wise_transfer.sourceValue))
        self.to_amount = Decimal(str(wise_transfer.targetValue))
        self.recipient = recipient
        self.exchange_rate = ExchangeRate(Decimal(str(wise_transfer.rate)), self.from_currency, self.to_currency)
        self.is_successful = wise_fund.status == "COMPLETED"
        self.error_message = wise_fund.errorMessage
        self.error_code = wise_fund.errorCode

    @classmethod
    def execute(cls, amount: Decimal, from_currency: global_common.Currency, to_currency: global_common.Currency, recipient_account_number: str, reference: str, profile_type: ProfileTypes) -> "Transfer":
        recipient: Recipient = Recipient.get_by_account_number_and_profile_type(recipient_account_number, profile_type)
        user_profile: UserProfile = UserProfile.get_by_profile_type(profile_type)
        wise_quote: wise_models.Quote = wise_models.Quote.call(user_profile.id, from_currency.value, to_currency.value, float(amount), recipient.account_id)
        wise_transfer: wise_models.Transfer = wise_models.Transfer.call(recipient.account_id, wise_quote.id, reference)
        wise_fund: wise_models.Fund = wise_models.Fund.call(user_profile.id, wise_transfer.id)
        return Transfer(user_profile, recipient, wise_transfer, wise_fund)

