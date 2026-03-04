from rest_framework import serializers

from store.models import Product
from store.output_serializers.product_photo_output_serializer import ProductPhotoOutputSerializer


class ProductOutputSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username")
    product_photos = ProductPhotoOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["product_id", "owner_username", "name", "description", "price", "amount", "color", "weight", "length", "width",
            "height", "guarantee_period", "status", "product_photos"]
