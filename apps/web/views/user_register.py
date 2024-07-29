from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from apps.web.models import User
from apps.web.serializers import UserSerializer
from rest_framework.permissions import AllowAny

class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                "message": "User registered successfully",
                "user": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Retrieve a user instance.
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update a user instance.
        """
        response = super().put(request, *args, **kwargs)
        response.data = {
            "message": "User updated successfully",
            "user": response.data
        }
        return response

    def patch(self, request, *args, **kwargs):
        """
        Partially update a user instance.
        """
        response = super().patch(request, *args, **kwargs)
        response.data = {
            "message": "User updated successfully",
            "user": response.data
        }
        return response