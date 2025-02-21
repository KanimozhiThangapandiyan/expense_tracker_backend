from django.db import models
from apps.common.models import Base
from apps.web.models import User
from auditlog.registry import auditlog

class Budget(Base):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Budget for {self.user_id} from {self.start_date} to {self.end_date} - Amount: {self.amount}"
auditlog.register(Budget)
