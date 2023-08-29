from main import BudgetService, IBudgetRepo, Budget
from datetime import datetime


class MockBudgetRepo(IBudgetRepo):
    def __init__(self, budgets: list[Budget]):
        self.budgets = budgets

    def getAll(self) -> list[Budget]:
        return self.budgets


def create_budget_list(budget_data_list: list[tuple[str, int]]) -> list[Budget]:
    return [create_buget(i[0], i[1]) for i in budget_data_list]


def create_buget(year_month: str, amount: int) -> Budget:
    budget = Budget()
    budget.YearMonth = year_month
    budget.Amount = amount
    return budget


def get_buget_service(budget_data_list):
    budget_list = create_budget_list(budget_data_list)
    return BudgetService(MockBudgetRepo(budget_list))


def test_get_one_range_data():
    budget_service = get_buget_service([("201901", 31), ("201902", 2000)])
    st, et = get_month_range("20190101", "20190101")
    range_data = budget_service.get_budget_range(st, et)
    assert len(range_data) == 1


def get_month_range(st: str, et: str) -> tuple[datetime, datetime]:
    return datetime.strptime(st, "%Y%m%d"), datetime.strptime(et, "%Y%m%d")


def test_get_two_range_data():
    budget_service = get_buget_service(
        [("201901", 31), ("201902", 2000), ("201903", 3100)]
    )
    st, et = get_month_range("20190101", "20190201")
    range_data = budget_service.get_budget_range(st, et)
    assert len(range_data) == 2


def test_one_day_calculate_amount():
    budget_service = get_buget_service([("201901", 31)])
    st, et = get_month_range("20190101", "20190101")
    range_data = budget_service.get_budget_range(st, et)
    amount = budget_service.calculate_amount(range_data, st, et)
    assert amount == 1


def test_n_day_calculate_amount():
    budget_service = get_buget_service([("201901", 31)])
    st, et = get_month_range("20190101", "20190110")
    range_data = budget_service.get_budget_range(st, et)
    amount = budget_service.calculate_amount(range_data, st, et)
    assert amount == 10


def test_cross_month_calculate_amount():
    budget_service = get_buget_service([("201903", 31), ("201904", 3000)])
    st, et = get_month_range("20190321", "20190410")
    range_data = budget_service.get_budget_range(st, et)
    amount = budget_service.calculate_amount(range_data, st, et)
    assert amount == 2100


def test_cross_two_months_calculate_amount():
    budget_service = get_buget_service(
        [("201903", 31), ("201904", 3000), ("201905", 31000)]
    )
    st, et = get_month_range("20190321", "20190515")
    range_data = budget_service.get_budget_range(st, et)
    amount = budget_service.calculate_amount(range_data, st, et)
    assert amount == 16100
