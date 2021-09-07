import datetime
import time
import typing
from decimal import Decimal
from typing import List, Any, Union

from ibapi.contract import Contract
from ibapi.order import Order

from ibkr import IBKR_API, connect_to_ib_api
from ibkr.exceptions import IBKR_APITimeOutException

if typing.TYPE_CHECKING:
    from ibkr.models import OrderAction, OrderType, HistoricalData, SecurityType


class IBKR_Helper:
    @staticmethod
    def get_data_from_ibkr(ibkr_api: IBKR_API, key_to_wait_for: str, data_key: str = None) -> List[Any]:
        data: List = None
        for _ in range(1, 60):
            data = ibkr_api.data.get(key_to_wait_for)

            if data is not None:
                break
            else:
                time.sleep(1)

        # ibkr_api.disconnect()

        if data is None:
            raise IBKR_APITimeOutException()

        return ibkr_api.data.get(key_to_wait_for) if data_key is None else ibkr_api.data.get(data_key)

    @staticmethod
    def get_IBKR_connection() -> IBKR_API:
        ibkr_api = IBKR_API()
        connect_to_ib_api(ibkr_api)
        return ibkr_api

    @staticmethod
    def get_contract_object(symbol: str, security_type: "SecurityType") -> Contract:
        contract = Contract()
        contract.symbol = symbol
        contract.secType = security_type.value
        contract.exchange = "SMART"
        contract.currency = "USD"

        from ibkr.models import SecurityType
        if security_type == SecurityType.STOCK:
            contract.primaryExchange = "NASDAQ"
        return contract

    @staticmethod
    def get_order_object(quantity: Decimal, limit_price: Decimal, order_action: "OrderAction", order_type: "OrderType") -> Order:
        order = Order()
        order.action = order_action.value
        order.orderType = order_type.value
        order.totalQuantity = int(quantity)
        order.outsideRth = True

        if order_type.value != "MKT" or limit_price is not None:
            order.lmtPrice = float(limit_price)
        return order


class HistoricalDataHelper:
    @staticmethod
    def filter_historical_data_list(starting_date: Union[datetime.datetime, str], ending_date: Union[datetime.datetime, str], historical_data_list: List["HistoricalData"]) -> List["HistoricalData"]:

        if isinstance(starting_date, str):
            starting_date = datetime.datetime.strptime(starting_date, '%Y-%m-%d')

        if ending_date is None:
            ending_date = datetime.datetime.today()
        elif isinstance(ending_date, str):
            ending_date = datetime.datetime.strptime(ending_date, '%Y-%m-%d')

        return_historical_data: List["HistoricalData"] = []
        for historical_data in historical_data_list:
            if starting_date <= historical_data.datetime <= ending_date:
                return_historical_data.append(historical_data)

        return_historical_data.sort(key=lambda x: x.datetime)
        return return_historical_data



