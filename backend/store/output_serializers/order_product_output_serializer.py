from rest_framework import serializers

from store.models import OrderProduct

class OrderProductOutputSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source="seller.username")
    product_id = serializers.IntegerField(source="product.product_id")
    transaction_id = serializers.IntegerField(source="transaction.transaction_id")

    class Meta:
        model = OrderProduct
        fields = ["order_product_id", "transaction_id", "product_id", "seller_username", "shopping_price"]
