from rest_framework import generics,status
from apps.expenses.models import Budget
from apps.expenses.serializers import BudgetSerializer
from rest_framework.response import Response

class BudgetLCView(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        start_date = request.data.get('start_date')

        # Check if the user already has an active budget
        active_budget_exists = Budget.objects.filter(
            user_id=user_id,
            end_date__gte=start_date
        ).exists()

        if active_budget_exists:
            return Response({
                'status': 'error',
                'message': 'You already have an active budget. You can only create a new budget after the current budget period has ended.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status': 'success',
            'message': 'Budget created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class BudgetRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Budget updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Budget deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
