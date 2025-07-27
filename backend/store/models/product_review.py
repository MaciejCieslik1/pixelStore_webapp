from django.db import models

class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=False)
    description = models.CharField(max_length=1024, null=False)
    reviewer_id = models.IntegerField(null=False)
    review_date = models.DateField(null=False)

    def __str__(self):
        return "Rating: " + str(self.rating)
