from rest_framework import serializers

from store.models import Product


class ProductOutputSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username")

    class Meta:
        model = Product
        fields = ["product_id", "owner_username", "name", "description", "price", "amount", "color", "weight", "length", "width",
            "height", "guarantee_period", "status"]
