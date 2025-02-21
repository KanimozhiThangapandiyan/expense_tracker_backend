from django.urls import path
from .views import UserListView,SoftDeleteUserView,UserDashboardView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/inactive/<int:pk>/', SoftDeleteUserView.as_view(), name='user-soft-delete'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard')
]
