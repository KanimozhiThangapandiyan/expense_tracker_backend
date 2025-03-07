from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.access.views import RegisterUserView,UserDetailView,AuthenticateUserView,LogoutView,KeycloakLoginView,\
    RoleViewSet,PermissionViewSet,ContentTypeListView

router = DefaultRouter()
router.register(r'role', RoleViewSet)
router.register(r'permission', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', RegisterUserView.as_view(), name='register_user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='retrieve-update-user-detail'),
    path('login/', AuthenticateUserView.as_view(), name='authenticate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('kc-login/', KeycloakLoginView.as_view(), name='kc-authentication'),
    path('models/', ContentTypeListView.as_view(), name='model-list'),
]
