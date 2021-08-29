import datetime
import time
import typing
from decimal import Decimal
from typing import List, Any

from ibapi.contract import Contract
from ibapi.order import Order

from ibkr import IBKR_API, connect_to_ib_api

if typing.TYPE_CHECKING:
    from ibkr.models import OrderAction, OrderType, InvestmentAnalysis, HistoricalData


class IBKR_Helper:
    @staticmethod
    def get_data_from_ibkr(ibkr_api: IBKR_API, key_to_wait_for: str, data_key: str = None) -> List[Any]:
        while ibkr_api.data.get(key_to_wait_for) is None:
            time.sleep(1)

        ibkr_api.disconnect()
        if data_key is None:
            return ibkr_api.data.get(key_to_wait_for)
        else:
            return ibkr_api.data.get(data_key)

    @staticmethod
    def get_IBKR_connection() -> IBKR_API:
        ibkr_api = IBKR_API()
        connect_to_ib_api(ibkr_api)
        return ibkr_api

    @staticmethod
    def get_contract_object(symbol: str) -> Contract:
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.primaryExchange = "NASDAQ"
        contract.currency = "USD"
        return contract

    @staticmethod
    def get_order_object(quantity: Decimal, limit_price: Decimal, order_action: "OrderAction", order_type: "OrderType") -> Order:
        order = Order()
        order.action = order_action.value
        order.orderType = order_type.value
        order.totalQuantity = int(quantity)
        order.outsideRth = True
        if not order_type == OrderType.MARKET or limit_price is not None:
            order.lmtPrice = str(limit_price)
        return order


class HistoricalDataHelper:
    @staticmethod
    def filter_historical_data_list(from_date_str: str, to_date_str: str, historical_data_list: List["HistoricalData"]) -> List["HistoricalData"]:
        from_date: datetime.datetime = datetime.datetime.strptime(from_date_str, '%Y-%m-%d')
        if to_date_str is not None:
            to_date: datetime.datetime = datetime.datetime.strptime(to_date_str, '%Y-%m-%d')
        else:
            to_date = datetime.datetime.today()

        return_historical_data: List["HistoricalData"] = []
        for historical_data in historical_data_list:
            if from_date <= historical_data.datetime <= to_date:
                return_historical_data.append(historical_data)
        return return_historical_data


class InvestmentAnalysisHelper:

    @staticmethod
    def get_number_of_years(investment_analysis: "InvestmentAnalysis") -> Decimal:
        number_of_whole_years: Decimal = Decimal((investment_analysis.ending_date.year - investment_analysis.starting_date.year))
        starting_date_reference: datetime.datetime = datetime.datetime(year=2000, month=investment_analysis.starting_date.month, day=investment_analysis.starting_date.day)
        ending_date_reference: datetime.datetime = datetime.datetime(year=2000, month=investment_analysis.ending_date.month, day=investment_analysis.ending_date.day)
        number_of_days = Decimal((ending_date_reference - starting_date_reference).days) + Decimal("1")
        return number_of_whole_years + (number_of_days / Decimal("365"))

    @staticmethod
    def get_annual_rate_of_return(investment_analysis: "InvestmentAnalysis") -> Decimal:
        a: Decimal = investment_analysis.ending_balance ** (1 / investment_analysis.number_of_years)
        b: Decimal = (1 / investment_analysis.starting_balance) ** (1 / investment_analysis.number_of_years)
        return (a * b) - Decimal("1")
