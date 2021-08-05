import os
from decimal import Decimal
from typing import Dict, Any, Optional, Type

import pandas
from numpy import ndarray
from pandas import DataFrame

from finance_database import common
from finance_database.exceptions import DataNotFoundException


class ExcelData:
    excel_data: DataFrame
    data: ndarray
    rows_start_index: int
    rows_end_index: int
    columns_size: int

    def __init__(self, excel_data: DataFrame):
        self.excel_data = excel_data
        self.data = self.excel_data.loc
        self.rows_start_index = self.excel_data.index.start
        self.rows_end_index = self.excel_data.index.stop
        self.columns_size = self.excel_data.columns.size

    def get(self, row: int, columns: int) -> "Data":
        return Data(self.data[row][columns], row, columns)

    def find(self, query_string: str) -> "Data":
        for row in range(self.rows_start_index, self.rows_end_index):
            for column in range(0, self.columns_size):
                data: Data = self.get(row, column)
                if data.data == query_string:
                    return data
        raise DataNotFoundException()

    def get_data_set(self, query_string: str) -> Dict[str, Any]:
        header: Data = self.find(query_string)
        data_set: Dict[str, Any] = {}

        value: Any = ""
        row_number: int = 1
        while value is not None and row_number <= self.columns_size:
            key: str = self.get(row_number + header.row, header.column).data
            value = self.get(row_number + header.row, header.column + 1).data
            if key is not None:
                data_set[key] = value
            row_number = row_number + 1

        return data_set

    def get_data_sub_set(self, query_string: str, number_of_datasets: int) -> "ExcelData":
        header: Data = self.find(query_string)
        end_column_number: int = header.column + (number_of_datasets * 2)
        end_row_number: Optional[int] = None

        row_number: int = header.row + 1
        while end_row_number is None:
            is_whole_row_nan: bool = True
            for column_number in range(header.column, end_column_number):
                is_whole_row_nan = is_whole_row_nan and self.get(row_number, column_number).data is None

            if is_whole_row_nan:
                end_row_number = row_number
            else:
                row_number = row_number + 1

        return ExcelData(self.excel_data.iloc[header.row:end_row_number, header.column:end_column_number])

    @classmethod
    def read_excel(cls: str, excel_file_path: str, sheet_name: str) -> "ExcelData":  # type: ignore
        temp_file_path: str = common.get_temp_file_path(excel_file_path)
        excel_data: ExcelData = ExcelData(pandas.read_excel(temp_file_path, sheet_name))
        os.remove(temp_file_path)
        return excel_data


class Data:
    data: Any
    row: int
    column: int

    def __init__(self, data: Any, row: int, column: int):
        self.row = row
        self.column = column

        if pandas.isna(data):
            self.data = None
        elif isinstance(data, (int, float, complex)) and not isinstance(data, bool):
            self.data = Decimal(str(data))
        else:
            self.data = data


class Summary:
    header: str = "Summary"
    salary: Decimal
    savings: Decimal
    needs: Decimal
    wants: Decimal
    refuse: Decimal

    def __init__(self, excel_data: ExcelData):
        summary_data: Dict[str, Decimal] = excel_data.get_data_set(self.header)
        self.salary = summary_data["Salary"]
        self.savings = summary_data["Savings"]
        self.needs = summary_data["Needs"]
        self.wants = summary_data["Wants"]
        self.refuse = summary_data["Refuse"]
        self.assert_accuracy()

    def assert_accuracy(self) -> None:
        assert self.salary == (self.savings + self.needs + self.wants + self.refuse)


class MonthlyExpenseReport:
    header: str = "Monthly Expense Report"
    needs: Decimal
    wants: Decimal
    savings: Decimal

    def __init__(self, excel_data: ExcelData):
        monthly_expense_report_data: Dict[str, Decimal] = excel_data.get_data_set(self.header)
        self.needs = monthly_expense_report_data["Needs"]
        self.wants = monthly_expense_report_data["Wants"]
        self.savings = monthly_expense_report_data["Savings"]

        self.assert_accuracy(excel_data)

    def assert_accuracy(self, excel_data: ExcelData) -> None:
        summary: Summary = Summary(excel_data)
        fixed_expenses: FixedExpenses = FixedExpenses(excel_data)
        assert summary.salary == self.needs + self.wants + self.savings + fixed_expenses.needs_expenses.total + \
               fixed_expenses.wants_expenses.total


class NeedsExpenses:
    header: str = "Needs"
    expenses: Dict[str, Decimal]
    total: Decimal

    def __init__(self, needs_expenses: Dict[str, Decimal]):
        self.expenses = needs_expenses

        self.total = Decimal("0")
        for expense in self.expenses.keys():
            self.total = self.total + self.expenses[expense]


class WantsExpenses:
    header: str = "Wants"
    expenses: Dict[str, Decimal]
    total: Decimal

    def __init__(self, wants_expenses: Dict[str, Decimal]):
        self.expenses = wants_expenses

        self.total = Decimal("0")
        for expense in self.expenses.keys():
            self.total = self.total + self.expenses[expense]


class FixedExpenses:
    header: str = "Fixed Expenses"
    needs_expenses: NeedsExpenses
    wants_expenses: WantsExpenses

    def __init__(self, excel_data: ExcelData):
        fixed_expenses_data: ExcelData = excel_data.get_data_sub_set(self.header, 2)
        self.needs_expenses = NeedsExpenses(fixed_expenses_data.get_data_set("Needs"))
        self.wants_expenses = WantsExpenses(fixed_expenses_data.get_data_set("Wants"))


class Transfer:
    bank_account: str
    description: str
    amount: Decimal

    def __init__(self, bank_account: str, description: str, amount: Decimal):
        self.bank_account = bank_account
        self.description = description
        self.amount = amount


class Transfers:
    finance_hub: Transfer
    needs: Transfer
    wants: Transfer
    savings: Transfer

    def __init__(self, excel_data: ExcelData):
        data: Dict[str, Any] = excel_data.get_data_set("Transfers")

        item_number: int = 1
        for transfer in data.items():
            bank_account: str = transfer[0]
            amount: Decimal = transfer[1]
            if item_number == 1:
                self.finance_hub = Transfer(bank_account, "Finance Hub", amount)
            elif item_number == 2:
                self.needs = Transfer(bank_account, "Needs", amount)
            elif item_number == 3:
                self.wants = Transfer(bank_account, "Wants", amount)
            elif item_number == 4:
                self.savings = Transfer(bank_account, "Savings", amount)
            item_number = item_number + 1

        assert Summary(
            excel_data).salary == self.finance_hub.amount + self.needs.amount + self.wants.amount + self.savings.amount
