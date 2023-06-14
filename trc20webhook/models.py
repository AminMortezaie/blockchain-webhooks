from django.db import models
from django.contrib.auth.admin import User


# based important fields off the token_callback_sample.json and coin_callback_sample.json files
# class Token(models.Model):
#     type = models.CharField(max_length=10)
#     name = models.CharField(max_length=100)
#     symbol = models.CharField(max_length=10)


class ConfirmedTransaction(models.Model):
    wallet_address = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=64)


class ConfirmedCoinTransaction(ConfirmedTransaction):
    coin_amount = models.CharField(max_length=100)


# I don't know how to use complex models with the DRF models!

# class ConfirmedTokenTransaction(ConfirmedTransaction):
#     token = models.ForeignKey(Token)
#     decimals = models.CharField(max_length=100)
#     token_amount = models.CharField(max_length=100)


class ConfirmedTokenTransaction(ConfirmedTransaction):
    toke_type = models.CharField(max_length=10)
    token_name = models.CharField(max_length=100)
    token_symbol = models.CharField(max_length=10)
    token_contractAddress: models.CharField(max_length=100)
    token_amount = models.CharField(max_length=100)
    decimals = models.CharField(max_length=100)
