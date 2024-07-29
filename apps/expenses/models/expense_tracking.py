from django.db import models
from apps.common.models import Base,MAX_LENGTH
from apps.web.models import User
from apps.expenses.models import ExpenseAndIncome 

class ExpenseTracking(Base):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    income_expense = models.ForeignKey(ExpenseAndIncome, on_delete=models.CASCADE)
    type = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return f"Tracking for {self.user} - {self.income_expense} - Type: {self.type}"
