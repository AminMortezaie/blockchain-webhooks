from django.contrib import admin
from django.urls import path
from trc20webhook.views import TransactionHistoryView


urlpatterns = [
    path('', TransactionHistoryView.as_view()),
]

