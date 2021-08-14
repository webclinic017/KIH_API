from finance_database import common
from finance_database.models import ExcelData, Transfers, FixedExpenses, MonthlyExpenseReport, Summary


class FinanceDatabase:
    summary: Summary
    monthly_expenses_report: MonthlyExpenseReport
    fixed_expenses: FixedExpenses
    transfers: Transfers

    def __init__(self, excel_file_path: str) -> None:
        excel_data: ExcelData = ExcelData.read_excel(excel_file_path, common.get_next_month_text())  # type: ignore
        self.summary = Summary(excel_data)
        self.monthly_expenses_report = MonthlyExpenseReport(excel_data)
        self.fixed_expenses = FixedExpenses(excel_data)
        self.transfers = Transfers(excel_data)
