class KeepAliveFailedException(Exception):
    pass


class AuthenticationFailedException(Exception):
    pass


class StockNotFoundException(Exception):
    pass


class MarketDataSnapshotNotAvailableException(Exception):
    pass


class MarketOrderOutsideRTHException(Exception):
    pass


class StockDataNotAvailableException(Exception):
    pass
