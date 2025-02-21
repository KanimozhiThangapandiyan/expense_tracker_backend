from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.access.models import User
from apps.cms.serializers import UsersSerializer
from rest_framework.pagination import PageNumberPagination

class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination


class SoftDeleteUserView(APIView):
    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk, is_deleted=False)
            user.delete()
            return Response({"message": "User has been successfully soft deleted."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
