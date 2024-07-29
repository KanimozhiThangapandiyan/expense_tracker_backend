from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.expenses.models import Budget, ExpenseAndIncome
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ExpenseTrackingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        current_date = timezone.now().date()

        # Get the current budget
        try:
            current_budget = Budget.objects.get(user_id=user.id, start_date__lte=current_date, end_date__gte=current_date)
        except Budget.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'No active budget found for the user.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Calculate total expenses within the budget period
        total_expenses = ExpenseAndIncome.objects.filter(
            user_id=user.id,
            type='expense',
            date__range=[current_budget.start_date, current_budget.end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Check if total expenses exceed or near 80% of the budget
        if total_expenses >= current_budget.amount:
            self.notify_user(user, 'You have exceeded your budget.')
        elif total_expenses >= 0.8 * current_budget.amount:
            self.notify_user(user, 'You have reached 80% of your budget.')

        return Response({
            'status': 'success',
            'total_expenses': total_expenses,
            'budget_amount': current_budget.amount,
            'message': 'Expense tracking completed.'
        }, status=status.HTTP_200_OK)

    def notify_user(self, user, message):
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email_id]
        send_mail(
            'Budget Notification',
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
