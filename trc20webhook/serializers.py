from rest_framework import serializers
from trc20webhook import models


# class BlockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Block
#         fields = '__all__'
#
#
# class TokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Token
#         fields = '__all__'


class ConfirmedCoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmedCoinTransaction
        fields = '__all__'


class ConfirmedTokenTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmedTokenTransaction
        fields = '__all__'
