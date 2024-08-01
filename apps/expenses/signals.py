from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
from apps.expenses.models import ExpenseAndIncome, Budget
from django.core.mail import send_mail
from django.conf import settings

def check_and_notify_budget(user):
    current_date = timezone.now().date()
    try:
        current_budget = Budget.objects.get(user_id=user.id, start_date__lte=current_date, end_date__gte=current_date)
    except Budget.DoesNotExist:
        return

    total_expenses = ExpenseAndIncome.objects.filter(
        user_id=user.id,
        type='expense',
        date__range=[current_budget.start_date, current_budget.end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email_id]
    if total_expenses >= current_budget.amount:    
        send_mail(
            'Budget Notification',
            'You have exceeded your budget.',
            from_email,
            recipient_list,
            fail_silently=False,
        )

    elif total_expenses >= 0.8 * current_budget.amount:
        send_mail(
            'Budget Notification',
            'You have reached 80% of your budget.',
            from_email,
            recipient_list,
            fail_silently=False,
        )

@receiver(post_save, sender=ExpenseAndIncome)
def update_expense_amount(sender, instance, created, **kwargs):
    if instance.type == 'expense':
        check_and_notify_budget(instance.user_id)