from django.contrib import admin
from .models import ConfirmedTransaction, ConfirmedCoinTransaction, \
            ConfirmedTokenTransaction, ConfirmedTokenTransaction,\
            TransactionHistory, Wallet, Network, Coin

admin.site.register(Network)
admin.site.register(Wallet)
admin.site.register(Coin)
admin.site.register(TransactionHistory)
admin.site.register(ConfirmedTransaction)
admin.site.register(ConfirmedCoinTransaction)
admin.site.register(ConfirmedTokenTransaction)
