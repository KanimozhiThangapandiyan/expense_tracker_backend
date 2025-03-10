from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.access.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import AllowAny,IsAuthenticated
from apps.cms.models import SystemLog
from django.contrib.auth.hashers import check_password
from apps.access.models import User
from apps.access.keycloak_utils import get_token,get_new_access_token
from django.shortcuts import get_object_or_404

class AuthenticateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email_id = request.data.get('email_id')
        password = request.data.get('password')

        try:
            user = User.objects.get(email_id=email_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        SystemLog.objects.create(user=user)

        return Response({
            "user": {
                "id": user.id,
                "email": user.email_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "date_of_birth": user.date_of_birth,
            },
            "token": token.key
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': 'User logged out successfully.'}, status=status.HTTP_200_OK)

class KeycloakLoginView(APIView):
    """APIView to authenticate user using Keycloak."""

    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email_id")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email_id=email)
        token = get_token(user.email_id, password)
        if not token:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(token, status=status.HTTP_200_OK)

class RefreshTokenAPIView(APIView):
    """API view to refresh the access token using the refresh token."""

    permission_classes = [AllowAny]
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        access_token, error = get_new_access_token(refresh_token)
        if access_token:
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": error},status=status.HTTP_401_UNAUTHORIZED)