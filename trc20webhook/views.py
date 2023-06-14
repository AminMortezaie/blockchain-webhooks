from rest_framework.views import APIView
from rest_framework.response import Response
from trc20webhook.models import TransactionHistory, RegisteredWallets
from trc20webhook.serializers import TransactionHistorySerializer, RegisterWalletSerializer
from trc20webhook.services.get_transaction_payload import generate_transaction
from trc20webhook.services.register_wallet_service import register_wallet


class TransactionHistoryView(APIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer

    def post(self, request):
        status_, transaction = generate_transaction(request)
        return Response({
            'message': transaction
        }, status=status_)


class RegisterWalletView(APIView):
    queryset = RegisteredWallets.objects.all()
    serializer_class = RegisterWalletSerializer

    def post(self, request):
        serializer = RegisterWalletSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        wallet = serializer_data['wallet']
        network = serializer_data['network']

        status_, message = register_wallet(network=network, wallet=wallet)
        return Response({
            'message': message
        }, status=status_)
