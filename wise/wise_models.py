import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from requests import Response

import http_requests
from http_requests import common
from http_requests.models import ResponseObject
from wise import constants


@dataclass
class UserProfileDetails:
    occupations: None = None
    acn: None = None
    abn: None = None
    arbn: None = None
    webpage: None = None
    businessSubCategory: None = None
    avatar: Optional[str] = None
    occupation: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    dateOfBirth: Optional[str] = None
    phoneNumber: Optional[str] = None
    primaryAddress: Optional[int] = None
    name: Optional[str] = None
    registrationNumber: Optional[str] = None
    companyType: Optional[str] = None
    companyRole: Optional[str] = None
    descriptionOfBusiness: Optional[str] = None
    businessCategory: Optional[str] = None
    firstNameInKana: Optional[str] = None
    lastNameInKana: Optional[str] = None


@dataclass
class UserProfiles(ResponseObject):
    id: Optional[int] = None
    type: Optional[str] = None
    details: Optional[UserProfileDetails] = None
    endpoint: str = constants.ENDPOINT_PROFILES

    @classmethod
    def call(cls) -> List["UserProfiles"]:
        response: Response = http_requests.get(cls.endpoint, headers=constants.HEADERS)
        user_profile_list: List[UserProfiles] = common.get_model_from_response(response, cls)  # type: ignore
        for user_profile in user_profile_list:
            user_profile.details = UserProfileDetails(**user_profile.details)  # type: ignore

        return user_profile_list


@dataclass
class Amount:
    value: Optional[float] = None
    currency: Optional[str] = None


@dataclass
class BankAddress:
    stateCode: None
    postCode: Optional[int] = None
    addressFirstLine: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


@dataclass
class BankDetails:
    id: Optional[int] = None
    currency: Optional[str] = None
    bankCode: Optional[str] = None
    accountNumber: Optional[str] = None
    swift: Optional[str] = None
    iban: Optional[str] = None
    bankName: Optional[str] = None
    accountHolderName: Optional[str] = None
    bankAddress: Optional[BankAddress] = None


@dataclass
class Balance:
    id: Optional[int] = None
    balanceType: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[Amount] = None
    reservedAmount: Optional[Amount] = None
    bankDetails: Optional[BankDetails] = None

    def __init__(self, id: int, balanceType: str, currency: str, amount: str, reservedAmount: Dict[str, Any], bankDetails: Dict[str, Any]):
        self.id = id
        self.balanceType = balanceType
        self.currency = currency
        self.amount = Amount(**amount)  # type: ignore
        self.reservedAmount = Amount(**reservedAmount)


@dataclass
class Account(ResponseObject):
    id: Optional[int] = None
    profileId: Optional[int] = None
    recipientId: Optional[int] = None
    creationTime: Optional[datetime] = None
    modificationTime: Optional[datetime] = None
    active: Optional[bool] = None
    eligible: Optional[bool] = None
    balances: Optional[List[Balance]] = None
    endpoint: str = constants.ENDPOINT_ACCOUNTS

    @classmethod
    def call(cls, profile_id: int) -> List["Account"]:
        response: Response = http_requests.get(cls.endpoint.replace("{profile_id}", str(profile_id)), headers=constants.HEADERS)
        accounts_list: List[Account] = common.get_model_from_response(response, cls)  # type: ignore

        for account in accounts_list:
            balances_list: List[Balance] = []
            for balance in account.balances:
                balances_list.append(Balance(**balance))  # type: ignore
            account.balances = balances_list

        return accounts_list


@dataclass
class ExchangeRate(ResponseObject):
    rate: Optional[float] = None
    source: Optional[str] = None
    target: Optional[str] = None
    time: Optional[str] = None
    endpoint: str = constants.ENDPOINT_EXCHANGE_RATES

    @classmethod
    def call(cls, source_currency: str = None, target_currency: str = None) -> "ExchangeRate":

        if source_currency is not None and target_currency is not None:
            response: Response = http_requests.get(cls.endpoint + f"?source={source_currency}&target={target_currency}", headers=constants.HEADERS)
        else:
            response = http_requests.get(cls.endpoint, headers=constants.HEADERS)

        return common.get_model_from_response(response, cls)[0]  # type: ignore


@dataclass
class Details:
    reference: Optional[str] = None


@dataclass
class Transfer(ResponseObject):
    transferRequest: None = None
    sourceAccount: None = None
    quote: None = None
    quoteUuid: Optional[UUID] = None
    id: Optional[int] = None
    user: Optional[int] = None
    targetAccount: Optional[int] = None
    status: Optional[str] = None
    reference: Optional[str] = None
    rate: Optional[float] = None
    created: Optional[datetime] = None
    business: Optional[int] = None
    details: Optional[Details] = None
    hasActiveIssues: Optional[bool] = None
    sourceCurrency: Optional[str] = None
    sourceValue: Optional[float] = None
    targetCurrency: Optional[str] = None
    targetValue: Optional[int] = None
    customerTransactionId: Optional[UUID] = None
    endpoint: str = constants.ENDPOINT_TRANSFER

    @classmethod
    def call(cls, target_account_id: int, quote_uuid: str, reference: str) -> "Transfer":
        parameters: Dict[str, Any] = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_uuid,
            "customerTransactionId": str(uuid.uuid4()),
            "details": {"reference": reference}
        }
        response: Response = http_requests.post(cls.endpoint, parameters=parameters, headers=constants.HEADERS)
        return common.get_model_from_response(response, cls)  # type: ignore


@dataclass
class DisabledReason:
    code: Optional[str] = None
    message: Optional[str] = None
    arguments: Optional[List[Any]] = None


@dataclass
class Fee:
    transferwise: Optional[float] = None
    payIn: Optional[float] = None
    discount: Optional[int] = None
    total: Optional[float] = None
    priceSetId: Optional[int] = None
    partner: Optional[int] = None


@dataclass
class PaymentOption:
    formattedEstimatedDelivery: Optional[str] = None
    estimatedDeliveryDelays: Optional[List[Any]] = None
    allowedProfileTypes: Optional[List[str]] = None
    feePercentage: Optional[float] = None
    estimatedDelivery: Optional[datetime] = None
    sourceAmount: Optional[float] = None
    targetAmount: Optional[int] = None
    sourceCurrency: Optional[str] = None
    targetCurrency: Optional[str] = None
    payOut: Optional[str] = None
    fee: Optional[Fee] = None
    payIn: Optional[str] = None
    disabled: Optional[bool] = None
    disabledReason: Optional[DisabledReason] = None


@dataclass
class HighAmount:
    showFeePercentage: Optional[bool] = None
    trackAsHighAmountSender: Optional[bool] = None
    showEducationStep: Optional[bool] = None
    offerPrefundingOption: Optional[bool] = None


@dataclass
class TransferFlowConfig:
    highAmount: Optional[HighAmount] = None


@dataclass
class Quote(ResponseObject):
    targetAmount: Optional[int] = None
    guaranteedTargetAmountAllowed: Optional[bool] = None
    targetAmountAllowed: Optional[bool] = None
    paymentOptions: Optional[List[PaymentOption]] = None
    notices: Optional[List[Any]] = None
    transferFlowConfig: Optional[TransferFlowConfig] = None
    rateTimestamp: Optional[datetime] = None
    clientId: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    profile: Optional[int] = None
    sourceCurrency: Optional[str] = None
    targetCurrency: Optional[str] = None
    rate: Optional[float] = None
    createdTime: Optional[datetime] = None
    user: Optional[int] = None
    rateType: Optional[str] = None
    rateExpirationTime: Optional[datetime] = None
    payOut: Optional[str] = None
    guaranteedTargetAmount: Optional[bool] = None
    providedAmountType: Optional[str] = None
    expirationTime: Optional[datetime] = None
    targetAccount: Optional[int] = None
    payInCountry: Optional[str] = None
    payOutCountry: Optional[str] = None
    funding: Optional[str] = None
    endpoint: str = constants.ENDPOINT_QUOTE

    @classmethod
    def call(cls, profile_id: int, source_currency: str, target_currency: str, target_amount: float, target_account_id: int) -> "Quote":
        parameters: Dict[str, Any] = {
            "profile": profile_id,
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": target_amount,
            "targetAccount": target_account_id,
            "payOut": "BALANCE"
        }
        response: Response = http_requests.post(cls.endpoint, parameters=parameters, headers=constants.HEADERS)
        return common.get_model_from_response(response, cls)  # type: ignore


@dataclass
class Address:
    country: None
    countryCode: None
    firstLine: None
    postCode: None
    city: None
    state: None


@dataclass
class RecipientDetails:
    accountHolderName: Optional[str] = None
    sortCode: Optional[str] = None
    abartn: Optional[str] = None
    accountType: Optional[str] = None
    bankgiroNumber: Optional[str] = None
    ifscCode: Optional[str] = None
    bsbCode: Optional[str] = None
    institutionNumber: Optional[str] = None
    transitNumber: Optional[str] = None
    phoneNumber: Optional[str] = None
    bankCode: Optional[str] = None
    russiaRegion: Optional[str] = None
    routingNumber: Optional[str] = None
    branchCode: Optional[str] = None
    cpf: Optional[str] = None
    cardToken: Optional[str] = None
    idType: Optional[str] = None
    idNumber: Optional[str] = None
    idCountryIso3: Optional[str] = None
    idValidFrom: Optional[str] = None
    idValidTo: Optional[str] = None
    clabe: Optional[str] = None
    dateOfBirth: Optional[str] = None
    clearingNumber: Optional[str] = None
    bankName: Optional[str] = None
    branchName: Optional[str] = None
    businessNumber: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    rut: Optional[str] = None
    token: Optional[str] = None
    cnpj: Optional[str] = None
    payinReference: Optional[str] = None
    pspReference: Optional[str] = None
    orderId: Optional[str] = None
    idDocumentType: Optional[str] = None
    idDocumentNumber: Optional[str] = None
    targetProfile: Optional[int] = None
    targetUserId: Optional[str] = None
    taxId: Optional[str] = None
    job: Optional[str] = None
    nationality: Optional[str] = None
    interacAccount: Optional[str] = None
    bban: Optional[str] = None
    town: Optional[str] = None
    postCode: Optional[str] = None
    language: Optional[str] = None
    billerCode: Optional[str] = None
    customerReferenceNumber: Optional[str] = None
    IBAN: Optional[str] = None
    iban: Optional[str] = None
    address: Optional[Address] = None
    email: Optional[str] = None
    legalType: Optional[str] = None
    accountNumber: Optional[str] = None
    swiftCode: Optional[str] = None
    bic: Optional[str] = None
    BIC: Optional[str] = None


@dataclass
class Recipient(ResponseObject):
    business: None = None
    id: Optional[int] = None
    profile: Optional[int] = None
    accountHolderName: Optional[str] = None
    type: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None
    details: Optional[RecipientDetails] = None
    user: Optional[int] = None
    active: Optional[bool] = None
    ownedByCustomer: Optional[bool] = None
    endpoint: str = constants.ENDPOINT_RECIPIENT_ACCOUNTS_LIST

    @classmethod
    def call(cls, profile_id: int) -> List["Recipient"]:
        response: Response = http_requests.get(cls.endpoint.replace("{profile_id}", str(profile_id)), headers=constants.HEADERS)
        recipient_list: List[Recipient] = common.get_model_from_response(response, cls)  # type: ignore
        for recipient in recipient_list:
            recipient.details = RecipientDetails(**recipient.details)  # type: ignore

        return recipient_list


@dataclass
class Fund(ResponseObject):
    type: Optional[str] = None
    status: Optional[str] = None
    errorCode: Optional[str] = None
    errorMessage: Optional[str] = None
    balanceTransactionId: Optional[int] = None
    endpoint: str = constants.ENDPOINT_FUND

    @classmethod
    def call(cls, profile_id: int, transfer_id: int) -> "Fund":
        response: Response = http_requests.post(cls.endpoint.replace("{profile_id}", str(profile_id)).replace("{transfer_id}", str(transfer_id)), parameters={"type": "BALANCE"}, headers=constants.HEADERS)
        return common.get_model_from_response(response, cls)  # type: ignore
