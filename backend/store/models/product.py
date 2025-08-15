from django.conf import settings
from django.db import models
from django.db.models.enums import TextChoices


class Product(models.Model):

    class ProductStatus(TextChoices):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        ARCHIVED = "archived"

    product_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='products')
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

    class Meta:
        db_table = 'product'
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return "Name: " + str(self)

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self.owner == other.owner and self.name == other.name and self.description == other.description and
                self.price == other.price and self.amount == other.amount and self.color == other.color and
                self.weight == other.weight and self.length == other.length and self.width == other.width and
                self.height == other.height and self.guarantee_period == other.guarantee_period and
                self.status == other.status)

    def __hash__(self):
        return hash((self.owner, self.name, self.description, self.price, self.amount, self.color, self.weight,
                self.length, self.width, self.height, self.guarantee_period, self.status))
