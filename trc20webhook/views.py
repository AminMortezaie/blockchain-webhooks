from rest_framework import generics
from rest_framework.response import Response
from trc20webhook import models, serializers


class ReceiveConfirmedCoinTransaction(generics.ListCreateAPIView):
    queryset = models.ConfirmedCoinTransaction.objects.all()
    serializer_class = serializers.ConfirmedCoinTransactionSerializer

    def post(self, request, *args, **kwargs):
        filtered_payload = {
            'wallet_address': request.data.get('data').get('item').get('address'),
            'transaction_id': request.data.get('data').get('item').get('transactionId'),
            'type': request.data.get('data').get('item').get('direction'),
            'coin_amount': request.data.get('data').get('item').get('amount')
        }
        serializer = self.get_serializer(data=filtered_payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Successful',
            'data': serializer.data
        })


class ReceiveConfirmedTokenTransaction(generics.ListCreateAPIView):
    queryset = models.ConfirmedTokenTransaction.objects.all()
    serializer_class = serializers.ConfirmedTokenTransactionSerializer

    def post(self, request, *args, **kwargs):
        filtered_payload = {
            'wallet_address': request.data.get('data').get('item').get('address'),
            'transaction_id': request.data.get('data').get('item').get('transactionId'),
            'toke_type': request.data.get('data').get('item').get('tokenType'),
            'token_name': request.data.get('data').get('item').get('token').get('name'),
            'token_symbol': request.data.get('data').get('item').get('token').get('symbol'),
            'token_contractAddress': request.data.get('data').get('item').get('token').get('contractAddress'),
            'type': request.data.get('data').get('item').get('direction'),
            'token_amount': request.data.get('data').get('item').get('token').get('amount'),
            'decimals': request.data.get('data').get('item').get('token').get('decimals'),
        }
        serializer = self.get_serializer(data=filtered_payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'message': 'Successful',
            'data': serializer.data
        })
