from django.db import models
from .product import Product

class ProductPhoto(models.Model):
    product_photo_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_photos')
    image_url = models.CharField(max_length=2048, null=False)
    is_main_photo = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_photo'

    def __str__(self):
        return "image_url: " + str(self.image_url)

    def __eq__(self, other):
        if not isinstance(other, ProductPhoto):
            return NotImplemented
        return (self.product == other.product and self.image_url == other.image_url and
                self.is_main_photo == other.is_main_photo)

    def __hash__(self):
        return hash((self.product, self.image_url, self.is_main_photo))
