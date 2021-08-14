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
    avatar: None
    occupation: None
    occupations: None
    first_name_in_kana: None
    last_name_in_kana: None
    acn: None
    abn: None
    arbn: None
    webpage: None
    business_sub_category: None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = None
    primary_address: Optional[int] = None
    name: Optional[str] = None
    registration_number: Optional[str] = None
    company_type: Optional[str] = None
    company_role: Optional[str] = None
    description_of_business: Optional[str] = None
    business_category: Optional[str] = None


@dataclass
class UserProfiles(ResponseObject):
    id: Optional[int] = None
    type: Optional[str] = None
    details: Optional[UserProfileDetails] = None
    endpoint: str = constants.ENDPOINT_PROFILES

    @classmethod
    def call(cls) -> List["UserProfiles"]:
        response: Response = http_requests.get(cls.endpoint, headers=constants.HEADERS)
        return common.get_model_from_response(response, cls)  # type: ignore


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
    balanceType: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[Amount] = None
    reservedAmount: Optional[Amount] = None
    bankDetails: Optional[BankDetails] = None


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
    def call(cls, profile_id: str) -> List["Account"]:
        response: Response = http_requests.get(cls.endpoint.replace("{profile_id}", str(profile_id)), headers=constants.HEADERS)
        return common.get_model_from_response(response, cls)  # type: ignore


@dataclass
class ExchangeRate(ResponseObject):
    rate: Optional[float] = None
    source: Optional[str] = None
    target: Optional[str] = None
    time: Optional[str] = None
    endpoint: str = constants.ENDPOINT_EXCHANGE_RATES

    @classmethod
    def call(cls, source_currency: str = None, target_currency: str = None) -> List["Account"]:

        if source_currency is not None and target_currency is not None:
            response: Response = http_requests.get(cls.endpoint + f"?source={source_currency}&target={target_currency}", headers=constants.HEADERS)
        else:
            response = http_requests.get(cls.endpoint, headers=constants.HEADERS)

        return common.get_model_from_response(response, cls)  # type: ignore


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
    id: Optional[UUID] = None
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
    email: None
    abartn: None
    accountType: None
    bankgiroNumber: None
    ifscCode: None
    bsbCode: None
    institutionNumber: None
    transitNumber: None
    phoneNumber: None
    bankCode: None
    russiaRegion: None
    routingNumber: None
    branchCode: None
    cpf: None
    cardNumber: None
    idType: None
    idNumber: None
    idCountryIso3: None
    idValidFrom: None
    idValidTo: None
    clabe: None
    swiftCode: None
    dateOfBirth: None
    clearingNumber: None
    bankName: None
    branchName: None
    businessNumber: None
    province: None
    city: None
    rut: None
    token: None
    cnpj: None
    payinReference: None
    pspReference: None
    orderId: None
    idDocumentType: None
    idDocumentNumber: None
    targetProfile: None
    taxId: None
    iban: None
    bic: None
    IBAN: None
    BIC: None
    interacAccount: None
    accountNumber: Optional[int] = None
    sortCode: Optional[int] = None
    address: Optional[Address] = None
    legalType: Optional[str] = None


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
        return common.get_model_from_response(response, cls)  # type: ignore


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
