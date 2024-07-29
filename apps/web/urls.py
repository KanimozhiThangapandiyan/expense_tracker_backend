from django.urls import path
from apps.web.views import RegisterUserView,UserDetailView,UserSystemLogListView,ExpenseAnalysisView

urlpatterns = [
    path('user/register/', RegisterUserView.as_view(), name='register_user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='retrieve-update-user-detail'),
    path('user/logs/', UserSystemLogListView.as_view(), name='user_system_logs'),
    path('user/analysis/', ExpenseAnalysisView.as_view(), name='expense-analysis'),
]
