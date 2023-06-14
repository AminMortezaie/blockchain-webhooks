from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from trc20webhook.models import TransactionHistory
from trc20webhook.serializers import TransactionHistorySerializer
from trc20webhook.services.get_transaction_payload import generate_transaction


class TransactionHistoryView(APIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer

    def post(self, request):
        status_, transaction = generate_transaction(request)
        return Response({
            'message': transaction
        }, status=status_)

