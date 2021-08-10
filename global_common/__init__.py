import datetime
import enum
import json
import threading
from decimal import Decimal
from typing import Any, Dict, Type, Optional, Callable

import database
import pytz
from ibkr.common import threads


def convert_string_to_dict(string: str) -> Dict[Any, Any]:
    parameters_list = string.split(",")

    return_dict = {}
    for parameter in parameters_list:
        key_value_pair = parameter.split("=")
        key = key_value_pair[0]
        value = key_value_pair[1]

        return_dict[key] = value

    return return_dict


def get_enum_from_value(value: Any, enum: Type[enum.Enum]) -> Optional[Any]:
    for enum_value in enum:
        if enum_value.value == value:
            return enum_value

    return None


def get_formatted_string_from_decimal(number: Decimal, decimal_places: int = 2) -> Decimal:
    return f'{number.quantize(Decimal(10) ** -decimal_places):,}'


def run_as_separate_thread(target: Callable, arguments: tuple = ()) -> None:
    return_function: threading.Thread = threading.Thread(target=target, args=arguments)
    return_function.start()
