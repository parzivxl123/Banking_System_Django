from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    reset_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.username



class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Received")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(max_length=50)

class Deposits(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deposits"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Withdrawals(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdrawals"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

