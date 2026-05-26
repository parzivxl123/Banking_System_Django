from django.urls import path
from .views import UserView, UserViewLimit, DepositView, WithdrawalView, DepositHistoryView, WithdrawalHistoryView

urlpatterns = [
    path("", UserView.as_view()),
    path("limit/<int:limit>/", UserViewLimit.as_view()),
    path("", UserView.as_view()),
    path(
        'deposit/',
        DepositView.as_view()
    ),

    path(
        'withdrawal/',
        WithdrawalView.as_view()
    ),
    path(
        "deposit/history/",
        DepositHistoryView.as_view()
    ),
    path(
        'withdrawal/history',
        WithdrawalHistoryView.as_view()
    ),

]