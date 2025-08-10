from django.db import models
from .product import Product

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, unique=True)
    description = models.CharField(max_length=1024, null=False)
    products = models.ManyToManyField(Product, related_name='categories', db_table='category_product')

    class Meta:
        db_table = 'category'

    def __str__(self):
        return "Name: " + self.name

    def __eq__(self, other):
        if not isinstance(other, Category):
            return NotImplemented
        return self.name == other.name and self.description == other.description

    def __hash__(self):
        return hash((self.name, self.description))
