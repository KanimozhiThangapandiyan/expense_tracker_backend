from django.urls import path
from .views import AuthenticateUserView,UserListView,SoftDeleteUserView,UserDashboardView,LogoutView

urlpatterns = [
    path('login/', AuthenticateUserView.as_view(), name='token_obtain_pair'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/inactive/<int:pk>/', SoftDeleteUserView.as_view(), name='user-soft-delete'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
