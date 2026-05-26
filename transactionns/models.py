from django.db import models

# Create your models here.
from users.models import User

class Transaction(models.Model):

    receiver =  models.ForeignKey(
        User,
        on_delete=  models.CASCADE,
        related_name ='received_transactions'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_transactions'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status=models.CharField(
        max_length=20,
        default="completed"
    )

    created_at = models.TimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username}->{self.receiver.username}"