from django.contrib import admin
from django.urls import path
from trc20webhook import views


urlpatterns = [
    path('coin/', views.ReceiveConfirmedCoinTransaction.as_view()),
    path('token/', views.ReceiveConfirmedTokenTransaction.as_view())
]

