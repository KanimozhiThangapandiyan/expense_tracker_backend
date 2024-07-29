from django.contrib import admin
from apps.web.models import User
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.unregister(Group)
