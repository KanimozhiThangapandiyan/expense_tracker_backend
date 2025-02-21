from rest_framework import generics
from apps.expenses.models import ExpenseAndIncome
from apps.expenses.serializers import ExpenseAndIncomeSerializer
from rest_framework import status
from django.http import JsonResponse

class ExpenseAndIncomeLCView(generics.ListCreateAPIView):
    queryset = ExpenseAndIncome.objects.all()
    serializer_class = ExpenseAndIncomeSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success","message": "created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseAndIncomeRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseAndIncome.objects.all()
    serializer_class = ExpenseAndIncomeSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success","message": "updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": "success","message": "partially updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({"status": "success", "message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
