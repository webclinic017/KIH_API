import enum
import time
from decimal import Decimal
from typing import Any, Dict

from ibapi.contract import Contract
from ibapi.order import Order

from ibkr import IBKR_API, connect_to_ib_api


class OrderType(enum.Enum):
    MARKET: str = "MKT"
    LIMIT: str = "LMT"


class OrderAction(enum.Enum):
    BUY: str = "BUY"
    SELL: str = "SELL"


class IBKR:
    pass


class IBKR_Helper:
    @staticmethod
    def get_data_from_ibkr(ibkr_api: IBKR_API, key_to_wait_for: str) -> Dict[str, Any]:
        while not ibkr_api.data.get("key") == key_to_wait_for:
            time.sleep(1)

        ibkr_api.disconnect()
        return ibkr_api.data

    @staticmethod
    def get_current_ask_price(symbol: str) -> Dict[str, Any]:
        contract = IBKR_Helper.get_contract_object(symbol)

        ibkr_api = IBKR_API()
        connect_to_ib_api(ibkr_api)
        ibkr_api.reqMktData(1, contract, '', False, False, [])
        return IBKR_Helper.get_data_from_ibkr(ibkr_api, "ask_price")["data"]["price"]

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
    def get_order_object(quantity: Decimal, limit_price: Decimal, order_action: OrderAction, order_type: OrderType) -> Order:
        order = Order()
        order.action = order_action.value
        order.orderType = order_type.value
        order.totalQuantity = int(quantity)
        if not order_type == OrderType.MARKET or limit_price is not None:
            order.lmtPrice = str(limit_price)
        return order

    @staticmethod
    def place_order(symbol: str, quantity: Decimal, limit_price: Decimal, order_action: OrderAction, order_type: OrderType) -> None:
        order: Order = IBKR_Helper.get_order_object(quantity, limit_price, order_action, order_type)
        contract: Contract = IBKR_Helper.get_contract_object(symbol)

        ibkr_api = IBKR_API()
        connect_to_ib_api(ibkr_api)
        ibkr_api.placeOrder(ibkr_api.next_order_id, contract, order)
        data: Dict[str, Any] = IBKR_Helper.get_data_from_ibkr(ibkr_api, "order_status")


if __name__ == "__main__":
    # IBKR_Helper.place_order("TQQQ", Decimal("1"), None, OrderAction.BUY, OrderType.MARKET)
    print(IBKR_Helper.get_current_ask_price("TQQQ"))
