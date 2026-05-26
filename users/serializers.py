from os import write
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Deposits, Withdrawals


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extrakwargs = {
            'password':{
                'writeonly':True
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            balance=validated_data.get(
                'balance',
                0
            )
        )

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits
        fields = "__all__"

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawals
        fields = "__all__"
