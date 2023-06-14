from rest_framework import serializers
from trc20webhook.models import TransactionHistory, RegisteredWallets


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'


class RegisterWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredWallets
        fields = '__all__'
