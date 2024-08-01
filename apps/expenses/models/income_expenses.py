from django.db import models
from apps.common.models import Base,DEFAULT_NULLABLE,SingleChoiceField
from apps.web.models import User
from auditlog.registry import auditlog

AMOUNT_TYPE_CHOICES = {
    "options": [
        "income",
        "expense"
    ],
}

CATEGORY_CHOICES ={
    "options": [
        "food",
        "transportation",
        "cosmetics",
        "entertainment",
        "housing",
        "utilities",
        "insurance",
        "healthcare",
        "dept_repayment",
        "savings",
        "miscellaneous",
        "others"
    ],
}

SPENDING_TYPE_CHOICES = {
    "options": [
        "debitcard",
        "creditcard",
        "cash"
    ],
}

class ExpenseAndIncome(Base):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = SingleChoiceField(choices_config=AMOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    category = SingleChoiceField(choices_config=CATEGORY_CHOICES, **DEFAULT_NULLABLE)
    spending_type = SingleChoiceField(choices_config=SPENDING_TYPE_CHOICES, **DEFAULT_NULLABLE)
    receipt_image = models.ImageField(upload_to='receipts/', **DEFAULT_NULLABLE)


    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount}"
auditlog.register(ExpenseAndIncome)