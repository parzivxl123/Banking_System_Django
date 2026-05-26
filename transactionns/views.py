from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from .serializers import TranssactionSerializer
from users.models import User
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

class TransactionView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        transaction = Transaction.objects.all()
        serializer = TranssactionSerializer(
            transaction,
            many = True
        )
        return Response(
            serializer.data
        )

    @transaction.atomic
    def post(self,request):
        sender = request.user
        receiverid = request.data.get(
            'receiver'
        )
        amount = Decimal(request.data.get(
            'amount'
        ))

        try:

            receiver =User.objects.get(
                id = receiverid
            )

        except User.DoesNotExist:
            return Response(
                {
                    "error":"User Not Found"
                },
                status=404
            )
        if sender==receiver:
            return Response(
                {
                    "error":"Sender cannot be same as receiver"
                 },
                status=400
            )
        if sender.balance < amount:
            return Response(
                {
                    "error":"Insufficien Balance"
                },
                status=400
            )
        if amount <=0:
            return Response(
                {
                    "error" : "insufficient amount"
                }
            )

        sender.balance-= amount
        receiver.balance+= amount
        sender.save()
        receiver.save()

        transaction = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount
        )
        serializer = TranssactionSerializer(
            transaction
        )
        return Response(
            serializer.data
        )

class TransactionHistoryView(APIView):
    def get(self,request):
        user = request.user
        sentTransactions = Transaction.objects.filter(
            sender = user
        )
        receivedtransactions = Transaction.objects.filter(
            receiver=user
        )

        sentserializer = TranssactionSerializer(
            sentTransactions,
            many=True
        )
        receivedserializer = TranssactionSerializer(
            receivedtransactions,
            many=True
        )

        return Response({
            "user":user.username,
            "sent":sentserializer.data,
            "received":receivedserializer.data
        })