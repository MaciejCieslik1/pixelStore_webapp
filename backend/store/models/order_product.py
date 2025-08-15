from django.db import models
from .transaction import Transaction
from .product import Product
from .user import User

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sold_order_products')
    shopping_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    class Meta:
        db_table = 'order_product'

    def __str__(self):
        return "Shopping price: " + str(self.shopping_price)

    def __eq__(self, other):
        if not isinstance(other, OrderProduct):
            return NotImplemented
        return (self.transaction == other.transaction and self.product == other.product and
            self.seller == other.seller and self.shopping_price == other.shopping_price)

    def __hash__(self):
        return hash((self.transaction, self.product, self.seller, self.shopping_price))
