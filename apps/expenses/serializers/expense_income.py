from rest_framework import serializers
from apps.expenses.models import ExpenseAndIncome

class ExpenseAndIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseAndIncome
        fields = '__all__'
