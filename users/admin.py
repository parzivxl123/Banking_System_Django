from django.contrib import admin
from .models import User, Deposits, Withdrawals


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'balance'
    )

    search_fields = (
        'username',
        'email'
    )


@admin.register(Deposits)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'amount',
        'created_at'
    )

    search_fields = (
        'user__username',
    )

    list_filter = (
        'created_at',
    )


@admin.register(Withdrawals)
class WithdrawalAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'amount',
        'created_at'
    )

    search_fields = (
        'user__username',
    )

    list_filter = (
        'created_at',
    )