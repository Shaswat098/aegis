from rest_framework import serializers
from apps.transactions.models import Transaction

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "user",
            "amount",
            "location",
            "device",
            "ip_address",
            "timestamp",
            "external_id"
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value