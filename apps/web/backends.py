from django.contrib.auth.backends import BaseBackend
from apps.web.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email_id=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
    
        return None


# from django.contrib.auth.backends import ModelBackend
# from apps.web.models import User

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email_id=username)
#             print(user)
#         except User.DoesNotExist:
#             return None

#         if user.check_password(password):
#             return user
    
#         return None
