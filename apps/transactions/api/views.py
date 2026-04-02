from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.transactions.api.serializers import TransactionCreateSerializer
from apps.transactions.services.transaction_service import create_transaction

class TransactionCreateAPIView(APIView):

    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)

        if serializer.is_valid():
            transaction = create_transaction(serializer.validated_data)
            return Response(
                {
                    "message": "Transaction received",
                    "transaction_id": transaction.id,
                    "status": transaction.status
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)