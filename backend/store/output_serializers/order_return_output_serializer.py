from rest_framework import serializers

from store.models import OrderReturn


class OrderReturnOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderReturn
        fields = ["order_return_id", "order_product_id", "description", "return_date_time", "is_accepted"]
