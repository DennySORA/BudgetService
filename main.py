import calendar
from datetime import datetime
from calendar import monthrange
from abc import ABC, abstractmethod


class Budget:
    def __init__(self):
        self.YearMonth: str = ""
        self.Amount: int = 0


class IBudgetRepo(ABC):
    @abstractmethod
    def getAll(self) -> list[Budget]:
        pass


class BudgetService:
    def __init__(self, budget_repo: IBudgetRepo):
        self.budget_repo = budget_repo

    def get_budget_range(self, start: datetime, end: datetime) -> list[Budget]:
        return [
            budget
            for budget in self.budget_repo.getAll()
            if start <= datetime.strptime(budget.YearMonth, "%Y%m") <= end
        ]

    @staticmethod
    def days_in_month(date: datetime) -> int:
        return monthrange(date.year, date.month)[1]

    @staticmethod
    def daily_budget(budget: Budget) -> float:
        year, month = map(int, [budget.YearMonth[:4], budget.YearMonth[4:]])
        return budget.Amount / monthrange(year, month)[1]

    def calculate_amount(
        self, budgets: list[Budget], start: datetime, end: datetime
    ) -> float:
        if len(budgets) == 1:
            return self.daily_budget(budgets[0]) * ((end - start).days + 1)
        elif len(budgets) == 2:
            return (
                self.daily_budget(budgets[0])
                * (self.days_in_month(start) - start.day + 1)
                + self.daily_budget(budgets[1]) * end.day
            )
        else:
            return self.calculate_amount([budgets[0], budgets[-1]], start, end) + sum(
                budget.Amount for budget in budgets[1:-1]
            )

    def query(self, start: datetime, end: datetime) -> float:
        selected_budgets = self.get_budget_range(start, end)
        return self.calculate_amount(selected_budgets, start, end)
