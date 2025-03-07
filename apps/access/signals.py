from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.access.models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Expense Tracker'
        message = f"""
        Hi {instance.first_name},

        Welcome to Expense tracker platform! We are thrilled to have you join our community.

        Best regards,
        The Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email_id]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
