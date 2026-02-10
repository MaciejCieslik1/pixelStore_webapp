from rest_framework import serializers

from store.models import ProductReview


class ProductReviewOutputSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source="product.product_id")
    reviewer_username = serializers.CharField(source="reviewer.username")

    class Meta:
        model = ProductReview
        fields = ["product_review_id", "product_id", "reviewer_username", "rating", "description", "review_date"]
