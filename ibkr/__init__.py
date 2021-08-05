import datetime
import time

import http_requests
import logger
from ibkr import constants, common
from ibkr.exceptions import KeepAliveFailedException, AuthenticationFailedException
from ibkr.ibkr_models import Authentication, KeepAlive, ReAuthentication, PortfolioAccounts, SelectAccount

http_requests.is_ssl_certificate_verification_used = False


def keep_alive() -> None:
    while True:
        logger.info("Keeping alive: " + str(datetime.datetime.now()))
        authentication: Authentication = Authentication.call()
        logger.info("Authentication status: " + str(authentication.authenticated))
        if not authentication.authenticated or not authentication.is_successful:
            if not authenticate():
                raise AuthenticationFailedException()
        time.sleep(constants.KEEP_ALIVE_TIMEOUT_IN_SECONDS)


def authenticate() -> bool:
    return ReAuthentication.call().is_successful

try:
    SelectAccount.execute()
except Exception:
    pass
