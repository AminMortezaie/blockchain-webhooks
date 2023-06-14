from rest_framework import serializers
from trc20webhook.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'

