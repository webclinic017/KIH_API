import threading
import time
from typing import Dict, Any

from ibapi.client import EClient
from ibapi.common import TickAttrib
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.wrapper import EWrapper

from ibkr import constants


class IBKR_API(EWrapper, EClient):
    data: Dict[str, Any] = {}
    next_order_id: int

    def __init__(self) -> None:
        EClient.__init__(self, self)

    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: TickAttrib) -> None:
        self.data = {
            "key": "ask_price",
            "data": locals()
        }

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState: OrderState) -> None:
        self.data = {
            "key": "order_status",
            "data": locals()
        }

    def nextValidId(self, orderId: int) -> None:
        super().nextValidId(orderId)
        self.next_order_id = orderId
        self.data = {"next_order_id": orderId}


def connect_to_ib_api(ibkr_api: IBKR_API) -> None:
    ibkr_api.connect(constants.WEB_SOCKET_IP, constants.WEB_SOCKET_PORT, constants.CLIENT_ID)
    api_thread = threading.Thread(target=ibkr_api.run, daemon=True)
    api_thread.start()
    time.sleep(3)
