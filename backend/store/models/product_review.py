from django.conf import settings
from django.db import models
from .product import Product

class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=False)
    description = models.CharField(max_length=1024, null=False)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviewer')
    review_date = models.DateField(null=False)

    class Meta:
        db_table = 'product_review'

    def __str__(self):
        return "Rating: " + str(self.rating)
