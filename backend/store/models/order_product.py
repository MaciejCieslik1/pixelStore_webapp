from django.db import models

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField(null=False)
    product_id = models.IntegerField(null=False)
    seller_id = models.IntegerField(null=False)
    shopping_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return "Shopping price: " + str(self.shopping_price)
