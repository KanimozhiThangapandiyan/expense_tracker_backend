from django.urls import path
from apps.expenses.views import ExpenseAndIncomeLCView,ExpenseAndIncomeRUDView,GenerateReportView,\
    BudgetLCView,BudgetRUDView,ExpenseTrackingView


urlpatterns = [
    path('create/', ExpenseAndIncomeLCView.as_view(), name='exp-inc-create-list'),
    path('RUD/<int:pk>/', ExpenseAndIncomeRUDView.as_view(), name='expense-detail'),
    path('generate/report/',GenerateReportView.as_view(), name='geerate-report'),
    path('budget/create-list/',BudgetLCView.as_view(), name='budget-create-list'),
    path('budget/RUD/<int:pk>/',BudgetRUDView.as_view(), name='budget-RUD'),
    path('expense-track/',ExpenseTrackingView.as_view(), name='exp-track'),

]
