import datetime
import enum
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Union

from ibapi.common import BarData
from ibapi.contract import Contract
from ibapi.order import Order

import global_common
from ibkr.helper import IBKR_Helper, InvestmentAnalysisHelper, HistoricalDataHelper


class OrderType(enum.Enum):
    MARKET: str = "MKT"
    LIMIT: str = "LMT"


class OrderAction(enum.Enum):
    BUY: str = "BUY"
    SELL: str = "SELL"


class HistoricalDataType(enum.Enum):
    TRADES: str = "TRADES"
    MIDPOINT: str = "MIDPOINT"
    BID: str = "BID"
    ASK: str = "ASK"
    BID_ASK: str = "BID_ASK"
    ADJUSTED_LAST: str = "ADJUSTED_LAST"
    HISTORICAL_VOLATILITY: str = "HISTORICAL_VOLATILITY"
    OPTION_IMPLIED_VOLATILITY: str = "OPTION_IMPLIED_VOLATILITY"
    REBATE_RATE: str = "REBATE_RATE"
    FEE_RATE: str = "FEE_RATE"
    YIELD_BID: str = "YIELD_BID"
    YIELD_ASK: str = "YIELD_ASK"
    YIELD_BID_ASK: str = "YIELD_BID_ASK"
    YIELD_LAST: str = "YIELD_LAST"


class IBKR:
    @staticmethod
    def get_historical_data(symbol: str, historical_data_type: HistoricalDataType = HistoricalDataType.TRADES) -> List["HistoricalData"]:
        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqPositions()
        ibkr_api.reqHistoricalData(ibkr_api.next_order_id, IBKR_Helper.get_contract_object(symbol), (datetime.datetime.today()).strftime("%Y%m%d %H:%M:%S"), "20 Y", "1 day", historical_data_type.value, 1, 1, False, [])
        raw_historical_data_list: List[Dict[str, Any]] = IBKR_Helper.get_data_from_ibkr(ibkr_api, "historical_data_end", "historical_data")

        historical_data: List[HistoricalData] = []
        for raw_historical_data in raw_historical_data_list:
            historical_data.append(HistoricalData(raw_historical_data.get("bar")))
        return historical_data

    @staticmethod
    def get_current_ask_price(symbol: str) -> Union[Decimal, None]:
        contract = IBKR_Helper.get_contract_object(symbol)

        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqMktData(1, contract, '', False, False, [])
        data_list: List[Dict[str, Any]] = IBKR_Helper.get_data_from_ibkr(ibkr_api, "ask_price")
        for data in data_list:
            if data.get("price") != -1:
                return Decimal(str(data.get("price")))
        return None

    @staticmethod
    def place_order(symbol: str, quantity: Decimal, limit_price: Decimal, order_action: OrderAction, order_type: OrderType) -> List[Any]:
        order: Order = IBKR_Helper.get_order_object(quantity, limit_price, order_action, order_type)
        contract: Contract = IBKR_Helper.get_contract_object(symbol)

        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.placeOrder(ibkr_api.next_order_id, contract, order)
        return IBKR_Helper.get_data_from_ibkr(ibkr_api, "order_status")

    @staticmethod
    def request_account_summary(currency: global_common.Currency = None) -> List[Any]:
        ibkr_api = IBKR_Helper.get_IBKR_connection()

        if currency is None:
            ibkr_api.reqAccountSummary(1, "All", "$LEDGER")
        else:
            ibkr_api.reqAccountSummary(1, "All", f"$LEDGER:{currency.value}")

        return IBKR_Helper.get_data_from_ibkr(ibkr_api, "account_summary_end", "account_summary")

    @staticmethod
    def get_positions() -> List[Any]:
        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqPositions()

        return IBKR_Helper.get_data_from_ibkr(ibkr_api, "positions_end", "positions")

    @staticmethod
    def get_all_order_status() -> List[Any]:
        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqAllOpenOrders()

        return IBKR_Helper.get_data_from_ibkr(ibkr_api, "order_status_end", "order_status")

    @staticmethod
    def cancel_all_orders() -> None:
        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqGlobalCancel()
        ibkr_api.disconnect()

    @staticmethod
    def get_all_managed_accounts() -> List[str]:
        ibkr_api = IBKR_Helper.get_IBKR_connection()
        ibkr_api.reqManagedAccts()

        data_list: List[Any] = IBKR_Helper.get_data_from_ibkr(ibkr_api, "managed_accounts")
        return_data: List[str] = []
        for data in data_list:
            return_data.append(data.get("accountsList"))
        return return_data


@dataclass
class HistoricalData:
    average: Decimal
    close: Decimal
    datetime: datetime.datetime
    high: Decimal
    low: Decimal
    open: Decimal
    volume: Decimal

    def __init__(self, bar_data: BarData):
        self.average = Decimal(str(bar_data.average))
        self.close = Decimal(str(bar_data.close))
        self.high = Decimal(str(bar_data.high))
        self.low = Decimal(str(bar_data.low))
        self.open = Decimal(str(bar_data.open))
        self.volume = Decimal(str(bar_data.volume))
        self.datetime = datetime.datetime.strptime(bar_data.date, '%Y%m%d')

    @staticmethod
    def calculate_daily_leveraged_trading_return(symbol: str, starting_capital: Decimal, leverage: Decimal, from_date_str: str = None, to_date_str: str = None) -> "InvestmentAnalysis":
        historical_data_list: List["HistoricalData"] = IBKR.get_historical_data(symbol)

        if from_date_str is not None:
            historical_data_list = HistoricalDataHelper.filter_historical_data_list(from_date_str, to_date_str, historical_data_list)
        historical_data_list.sort(key=lambda x: x.datetime)

        number_of_shares_bought: Decimal = Decimal(0)
        loan_amount: Decimal = Decimal(0)
        net_liquidity: Decimal = Decimal(0)

        for historical_data in historical_data_list:
            if historical_data == historical_data_list[0]:
                cash_balance: Decimal = starting_capital
            else:
                cash_balance = (number_of_shares_bought * historical_data.close) - loan_amount

            number_of_shares_bought = Decimal(int((cash_balance * leverage) / historical_data.close))
            loan_amount = (number_of_shares_bought * historical_data.close) - cash_balance
            net_liquidity = (number_of_shares_bought * historical_data.close) - loan_amount

        return InvestmentAnalysis(historical_data_list[0].datetime, historical_data_list[-1].datetime, starting_capital, net_liquidity)


@dataclass
class InvestmentAnalysis:
    starting_date: datetime.datetime
    ending_date: datetime.datetime
    number_of_years: Decimal
    starting_balance: Decimal
    ending_balance: Decimal
    profit: Decimal
    annual_rate_of_return: Decimal

    def __init__(self, starting_date: datetime.datetime, ending_date: datetime.datetime, starting_balance: Decimal, ending_balance: Decimal):
        self.starting_balance = starting_balance
        self.ending_balance = ending_balance
        self.starting_date = starting_date
        self.ending_date = ending_date

        self.profit = self.ending_balance - self.starting_balance
        self.number_of_years = InvestmentAnalysisHelper.get_number_of_years(self)
        self.annual_rate_of_return = InvestmentAnalysisHelper.get_annual_rate_of_return(self)


if __name__ == "__main__":
    test = IBKR.get_all_managed_accounts()
    pass
