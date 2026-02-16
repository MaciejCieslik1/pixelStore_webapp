from rest_framework import serializers

from store.models import Transaction


class TransactionOutputSerializer(serializers.ModelSerializer):
    buyer_username = serializers.CharField(source="buyer.username")

    class Meta:
        model = Transaction
        fields = ["transaction_id", "buyer_username", "total_price", "date_time", "is_finished"]
