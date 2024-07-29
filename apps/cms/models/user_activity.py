from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SystemLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    login_time = models.DateTimeField(_("Login Time"), auto_now_add=True)

    class Meta:
        verbose_name = _("System Log")
        verbose_name_plural = _("System Logs")

    def __str__(self):
        return f"{self.user} logged in at {self.login_time}"
