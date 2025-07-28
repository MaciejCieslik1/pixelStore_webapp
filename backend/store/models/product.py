from django.db import models
from django.db.models.enums import TextChoices


class Product(models.Model):

    class ProductStatus(TextChoices):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        ARCHIVED = "archived"

    product_id = models.AutoField(primary_key=True)
    owner_id = models.IntegerField(null=False)
    name = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=1024, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    amount = models.IntegerField(null=False)
    color = models.CharField(max_length=32, null=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    guarantee_period = models.IntegerField(null=False)
    status = models.CharField(max_length=20, choices=ProductStatus.choices, default=ProductStatus.AVAILABLE, null=False)

    def __str__(self):
        return "Name: " + str(self)