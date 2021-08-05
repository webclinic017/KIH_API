import enum
import json
import time
from typing import Dict, Optional, Any

import requests
import urllib3
from requests import Response

import logger
import database.constants
import http_requests.constants as constants

is_ssl_certificate_verification_used: bool = True
urllib3.disable_warnings()


class MethodType(enum.Enum):
    GET: str = "GET"
    POST: str = "POST"
    PUT: str = "PUT"
    DELETE: str = "DELETE"


class ServerErrorException(Exception):
    pass


class ClientErrorException(Exception):
    pass


def get(url: str, parameters: Optional[Dict[str, Any]] = None) -> Response:
    return request(url, parameters, MethodType.GET)


def post(url: str, parameters: Optional[Dict[str, Any]] = None) -> Response:
    return request(url, parameters, MethodType.POST)


def put(url: str, parameters: Optional[Dict[str, Any]] = None) -> Response:
    return request(url, parameters, MethodType.PUT)

def delete(url: str, parameters: Optional[Dict[str, Any]] = None) -> Response:
    return request(url, parameters, MethodType.DELETE)

def request(url: str, parameters: Optional[Dict[str, Any]], method_type: MethodType, server_error_retry_times: int = 0) -> Response:
    global is_ssl_certificate_verification_used
    start_time: float = time.time()

    response: Response = None
    if method_type == MethodType.GET:
        response = requests.get(url=url, params=parameters, verify=is_ssl_certificate_verification_used)
    elif method_type == MethodType.POST:
        response = requests.post(url=url, json=parameters, verify=is_ssl_certificate_verification_used)
    elif method_type == MethodType.PUT:
        response = requests.put(url=url, params=parameters, verify=is_ssl_certificate_verification_used)
    elif method_type == MethodType.DELETE:
        response = requests.delete(url=url, params=parameters, verify=is_ssl_certificate_verification_used)

    if 400 <= response.status_code <= 499:
        print("Response code: " + str(response.status_code))
        raise ClientErrorException(response.text)
    elif 500 <= response.status_code <= 599:
        print("Response code: " + str(response.status_code))
        if server_error_retry_times < constants.SERVER_ERROR_RETRY_TIMES:
            print("Retrying")
            response = request(url, parameters, method_type, server_error_retry_times + 1)
        else:
            raise ServerErrorException(response.text)

    time_taken: int = int((time.time() - start_time) * 1000)
    logger.performance(constants.EXECUTION_TYPE_API_Call, method_type.value, response.url,
                       start_time, url)
    __log_webservice(url, parameters, response, time_taken)

    return response


def __log_webservice(url: str, parameters: Dict[str, Any], response: Response, time_taken: int) -> None:
    parameters = {database.constants.column_Log__Application: database.constants.database_application_name,
                  database.constants.column_API_Calls__URL: url,
                  database.constants.column_API_Calls__Response_Code: response.status_code,
                  database.constants.column_API_Calls__Parameters: str(json.dumps(parameters)).replace("\\n", ""),
                  database.constants.column_API_Calls__Response: response.text.replace("\\n", ""),
                  database.constants.column_API_Calls__Execution_Time: int(time_taken)}
    database.insert(database.constants.table_API_Calls, parameters)
