from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Deposits, Withdrawals
from .serializers import UserSerializer, DepositSerializer, WithdrawalSerializer
from django.contrib.auth.hashers import (
    check_password,
    make_password
)
from rest_framework.throttling import ScopedRateThrottle
from .throttles import LoginRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from .throttles import LoginRateThrottle, PasswordResetRateThrottle
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

    def get(self, request, user_id):

        try:
            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "User Not Found"
                },
                status=404
            )

        page = int(
            request.GET.get(
                "page",
                1
            )
        )

        page_size = int(
            request.GET.get(
                "page_size",
                10
            )
        )

        start = (
            page - 1
        ) * page_size

        end = start + page_size

        deposit_queryset = Deposits.objects.filter(
            user=user
        ).order_by("-id")

        deposits = deposit_queryset[
            start:end
        ]

        serializer = DepositSerializer(
            deposits,
            many=True
        )

        return Response(
            {
                "user":
                user.username,

                "page":
                page,

                "page_size":
                page_size,

                "total_deposits":
                deposit_queryset.count(),

                "deposits":
                serializer.data
            }
        )


class WithdrawalHistoryView(APIView):

    def get(self, request, user_id):

        try:
            user = User.objects.get(
                id=user_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "User Not Found"
                },
                status=404
            )

        page = int(
            request.GET.get(
                "page",
                1
            )
        )

        page_size = int(
            request.GET.get(
                "page_size",
                10
            )
        )

        start = (
            page - 1
        ) * page_size

        end = start + page_size

        withdrawal_queryset = Withdrawals.objects.filter(
            user=user
        ).order_by("-id")

        withdrawals = withdrawal_queryset[
            start:end
        ]

        serializer = WithdrawalSerializer(
            withdrawals,
            many=True
        )

        return Response(
            {
                "user":
                user.username,

                "page":
                page,

                "page_size":
                page_size,

                "total_withdrawals":
                withdrawal_queryset.count(),

                "withdrawals":
                serializer.data
            }
        )


class ForgotPasswordView(APIView):
    throttle_classes = [
        PasswordResetRateThrottle
    ]
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

        # 1. Define the HTML template using an f-string to inject the reset_link
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    background-color: #f4f7f6;
                    margin: 0;
                    padding: 0;
                    -webkit-font-smoothing: antialiased;
                }}
                .email-wrapper {{
                    width: 100%;
                    background-color: #f4f7f6;
                    padding: 40px 0;
                }}
                .email-content {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
                    overflow: hidden;
                }}
                .email-header {{
                    background-color: #2c3e50;
                    padding: 20px;
                    text-align: center;
                    color: #ffffff;
                }}
                .email-body {{
                    padding: 40px 30px;
                    color: #333333;
                    line-height: 1.6;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #3498db;
                    color: #ffffff !important;
                    text-decoration: none;
                    padding: 14px 28px;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .email-footer {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    text-align: center;
                    font-size: 13px;
                    color: #888888;
                    border-top: 1px solid #eeeeee;
                }}
                .link-fallback {{
                    font-size: 13px;
                    color: #888888;
                    word-break: break-all;
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="email-content">
                    <div class="email-header">
                        <h2 style="margin: 0;">Password Reset Request</h2>
                    </div>

                    <div class="email-body">
                        <p style="font-size: 16px;">Hello,</p>
                        <p style="font-size: 16px;">We received a request to reset the password for your account. If you made this request, please click the button below to set a new password:</p>

                        <div style="text-align: center;">
                            <a href="{reset_link}" class="btn">Reset My Password</a>
                        </div>

                        <p style="font-size: 16px;">If you did not request a password reset, you can safely ignore this email. Your account is secure and your password has not been changed.</p>

                        <hr style="border: none; border-top: 1px solid #eeeeee; margin: 30px 0;">

                        <p class="link-fallback">
                            If the button doesn't work, copy and paste this link into your web browser:<br>
                            <a href="{reset_link}" style="color: #3498db;">{reset_link}</a>
                        </p>
                    </div>

                    <div class="email-footer">
                        <p style="margin: 0;">&copy; 2026 Your Company Name. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # 2. Define the plain-text fallback (important for spam filters and accessibility)
        plain_message = f"""
        Password Reset Request

        Hello,

        We received a request to reset the password for your account. 
        Click the link below to set a new password:

        {reset_link}

        If you did not request a password reset, you can safely ignore this email.
        """

        # 3. Send the email utilizing the html_message parameter
        send_mail(
            subject="Password Reset",
            message=plain_message,  # The plain-text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message  # The amazing looking HTML version
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