import statistics
import typing
from datetime import datetime
from decimal import Decimal
from typing import List

from ibkr.models import HistoricalData
from typing import Tuple

if typing.TYPE_CHECKING:
    from investment_analysis.models import HistoricalData, HistoricalReturn


class InvestmentAnalysisHelper:

    @staticmethod
    def get_number_of_years(starting_date: datetime, ending_date: datetime) -> Decimal:
        number_of_whole_years: Decimal = Decimal((ending_date.year - starting_date.year))
        starting_date_reference: datetime = datetime(year=2000, month=starting_date.month, day=starting_date.day)
        ending_date_reference: datetime = datetime(year=2000, month=ending_date.month, day=ending_date.day)
        number_of_days = Decimal((ending_date_reference - starting_date_reference).days) + Decimal("1")
        return number_of_whole_years + (number_of_days / Decimal("365"))

    @staticmethod
    def get_annual_rate_of_return(starting_balance: Decimal, ending_balance: Decimal, number_of_years: Decimal) -> Decimal:
        a: Decimal = ending_balance ** (1 / number_of_years)
        b: Decimal = (1 / starting_balance) ** (1 / number_of_years)
        return (a * b) - Decimal("1")

    @staticmethod
    def get_leveraged_historical_data_list(starting_balance: Decimal, leverage: Decimal, historical_data_list: List["HistoricalData"]) -> List["HistoricalReturn"]:
        from investment_analysis.models import HistoricalReturn
        historical_returns_list: List[HistoricalReturn] = []

        number_of_shares_bought: Decimal = Decimal(0)
        loan_amount: Decimal = Decimal(0)
        for historical_data in historical_data_list:
            if historical_data == historical_data_list[0]:
                cash_balance: Decimal = starting_balance
            else:
                cash_balance = (number_of_shares_bought * historical_data.close) - loan_amount if number_of_shares_bought != Decimal(0) else cash_balance

            if cash_balance <= Decimal(0):
                historical_returns_list.append(HistoricalReturn(historical_data.datetime, Decimal(0), Decimal(0), historical_data.close))
                return historical_returns_list

            number_of_shares_bought = Decimal(int((cash_balance * leverage) / historical_data.close))
            loan_amount = (number_of_shares_bought * historical_data.close) - cash_balance if (number_of_shares_bought * historical_data.close) > cash_balance else Decimal(0)
            net_liquidity = (number_of_shares_bought * historical_data.close) - loan_amount if (number_of_shares_bought * historical_data.close) > cash_balance else cash_balance

            historical_returns_list.append(HistoricalReturn(historical_data.datetime, number_of_shares_bought, net_liquidity, historical_data.close))
        return historical_returns_list

    @staticmethod
    def get_number_of_days_till_no_loss(historical_returns_list: List["HistoricalReturn"]) -> Tuple[Decimal, Decimal]:
        starting_date: datetime = historical_returns_list[0].date
        lowest_net_liquidity: Decimal = historical_returns_list[0].net_liquidity
        number_of_days_till_no_loss: Decimal = Decimal(0)
        for historical_return in historical_returns_list:
            number_of_days_till_no_loss = Decimal((historical_return.date - starting_date).days) if historical_return.net_liquidity < lowest_net_liquidity else number_of_days_till_no_loss
            lowest_net_liquidity = historical_return.net_liquidity if historical_return.net_liquidity < lowest_net_liquidity else lowest_net_liquidity
        return number_of_days_till_no_loss, lowest_net_liquidity

    @staticmethod
    def add_years_to_date(date: datetime, number_of_years: Decimal) -> datetime:
        return_date: datetime = None
        try:
            return_date = date.replace(year=(date.year + int(number_of_years)))
        except ValueError as e:
            if str(e) == "day is out of range for month":
                return_date = date.replace(year=(date.year + int(number_of_years)), day=28)
            else:
                raise e
        return return_date
