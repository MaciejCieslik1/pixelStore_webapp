from rest_framework import serializers

from store.models import ProductPhoto


class ProductPhotoOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPhoto
        fields = ["product_photo_id", "image_url", "is_main_photo"]
