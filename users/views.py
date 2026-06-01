from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Deposits, Withdrawals
from .serializers import UserSerializer, DepositSerializer, WithdrawalSerializer
from django.contrib.auth.hashers import (
    check_password,
    make_password
)
from decimal import Decimal
import uuid
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
class UserView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(
            users,
               many = True
        )
        return Response(
            serializer.data
        )

    def post(self,request):
        serializer = UserSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(
            serializer.errors
        )

    def put(self, request):

        userid = request.data.get('userid')
        newusername = request.data.get('newusername')
        newemail = request.data.get('newemail')
        oldpassword = request.data.get('oldpassword')
        newpassword = request.data.get('newpassword')

        try:
            user = User.objects.get(
                id=userid
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User Not Found"
                },
                status=404
            )

        if not check_password(
                oldpassword,
                user.password
        ):
            return Response(
                {
                    "error": "Wrong Password"
                },
                status=401
            )

        if newusername:
            user.username = newusername

        if newemail:
            user.email = newemail

        if newpassword:
            user.password = make_password(
                newpassword
            )

        user.save()

        serializer = UserSerializer(
            user
        )

        return Response(
            serializer.data
        )
class UserViewLimit(APIView):
    def get(self,request,limit):
        uses = User.objects.all()[:int(limit)]
        serializer = UserSerializer(
            uses,
            many=True
        )
        return Response(
            serializer.data
        )

class DepositView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        amount = Decimal(
            request.data.get(
                "amount"
            )
        )
        if amount <= 0:
            return Response(
                {
                    "error":"Invalid amount"
                },
                status=400
            )

        user.balance += amount
        user.save()
        deposit = Deposits.objects.create(
            user=user,
            amount=amount
        )
        serializer = DepositSerializer(
            deposit
        )
        return Response(
            serializer.data
        )




class WithdrawalView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self,request):


        user = request.user

        amount = Decimal(
            request.data.get(
                "amount"
            )
        )

        if amount <= 0:

            return Response(
                {
                    "error":"Invalid amount"
                },
                status=400
            )

        if user.balance < amount:

            return Response(
                {
                    "error":"Insufficient balance"
                },
                status=400
            )

        user.balance -= amount

        user.save()

        withdrawal = Withdrawals.objects.create(
            user=user,
            amount=amount
        )

        serializer = WithdrawalSerializer(
            withdrawal
        )

        return Response(
            serializer.data
        )

class DepositHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        deposits = Deposits.objects.filter(
            user=request.user
        ).order_by(
            '-created_at'
        )

        serializer = DepositSerializer(
            deposits,
            many=True
        )
        return Response(
            serializer.data
        )


class WithdrawalHistoryView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    def get(self, request):

        withdrawals = Withdrawals.objects.filter(
            user=request.user
        ).order_by(
            '-created_at'
        )
        serializer = WithdrawalSerializer(
            withdrawals,
            many=True
        )
        return Response(
            serializer.data
        )


class ForgotPasswordView(APIView):
    def post(self,request):
        email = request.data.get(
            "email"
        )

        try:
            user = User.objects.get(
                email=email
            )
        except User.DoesNotExist:
            return Response(
                {
                    "error" : "User Not Found"
                },status=404
            )
        token = str(uuid.uuid4())
        user.reset_token = token
        user.save()

        reset_link = (
            f"http://127.0.0.1:8000/"
            f"users/reset-password/"
            f"?token={token}"
        )

        send_mail(
            "Password Reset",
            f"Click Below:\n\n{reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

        return Response({
            "Password Change Email Sent"
        })

class ResetPasswordView(APIView):
    def post(self,request):
        token = request.data.get("token")
        newpassword = request.data.get("newpassword")
        try:
            user = User.objects.get(
                reset_token=token
            )
        except User.DoesNotExist:
            return Response({
                "error" : "User Not Found"
            },status=404
            )

        user.password = make_password(
            newpassword
        )
        user.reset_token = None
        user.save()

        return Response(
            {
                "Password Updated"
            }
        )