from django.contrib import admin
from apps.expenses.models import Budget,ExpenseAndIncome

admin.site.register(Budget)
admin.site.register(ExpenseAndIncome)
