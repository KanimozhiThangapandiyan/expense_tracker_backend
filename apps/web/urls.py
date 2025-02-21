from django.urls import path
from apps.web.views import UserSystemLogListView,ExpenseAnalysisView

urlpatterns = [
    path('user/logs/', UserSystemLogListView.as_view(), name='user_system_logs'),
    path('user/analysis/', ExpenseAnalysisView.as_view(), name='expense-analysis'),
]
