from django.http import JsonResponse
from django.views import View
from apps.access.models import User

class UserDashboardView(View):
    def get(self, request, *args, **kwargs):
        active_users_count = User.objects.filter(is_deleted=False).count()
        inactive_users_count = User.objects.filter(is_deleted=True).count()

        data = {
            'active_users': active_users_count,
            'inactive_users': inactive_users_count,
        }
        return JsonResponse(data)
