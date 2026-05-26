from django.db import transaction
from django.urls import path
from .views import TransactionView, TransactionHistoryView

urlpatterns = [
    path('',TransactionView.as_view()    ),
    path('user/<int:user_id>/', TransactionHistoryView.as_view())
]