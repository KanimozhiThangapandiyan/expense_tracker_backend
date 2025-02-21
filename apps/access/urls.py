from django.urls import path
from apps.access.views import RegisterUserView,UserDetailView,AuthenticateUserView,LogoutView


urlpatterns = [
    path('user/register/', RegisterUserView.as_view(), name='register_user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='retrieve-update-user-detail'),
    path('login/', AuthenticateUserView.as_view(), name='authenticate'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
