from rest_framework import serializers
from trc20webhook.models import TransactionHistory, ConfirmedCoinTransaction, ConfirmedTokenTransaction


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'


class ConfirmedCoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedCoinTransaction
        fields = '__all__'


class ConfirmedTokenTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedTokenTransaction
        fields = '__all__'
