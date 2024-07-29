from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.web.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import AllowAny,IsAuthenticated
from apps.cms.models import SystemLog

class AuthenticateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email_id = request.data.get('email_id')
        password = request.data.get('password')

        try:
            user = User.objects.get(email_id=email_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
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