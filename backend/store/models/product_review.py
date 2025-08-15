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

    def __eq__(self, other):
        if not isinstance(other, ProductReview):
            return NotImplemented
        return (self.product == other.product and self.rating == other.rating and
                self.description == other.description and self.reviewer == other.reviewer and
                self.review_date == other.review_date)

    def __hash__(self):
        return hash((self.product, self.rating, self.description, self.reviewer, self.review_date))
