from django.db import models
from .order_product import OrderProduct

class OrderReturn(models.Model):
    order_return_id = models.AutoField(primary_key=True)
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='order_returns')
    description = models.CharField(max_length=1024, null=False)
    return_date_time = models.DateTimeField(null=False)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_return'
        indexes = [models.Index(fields=['return_date_time'])]

    def __str__(self):
        return "description: " + str(self.description)

    def __eq__(self, other):
        if not isinstance(other, OrderReturn):
            return NotImplemented
        return (self.order_product == other.order_product and self.description == other.description and
                self.return_date_time == other.return_date_time and self.is_accepted == other.is_accepted)

    def __hash__(self):
        return hash((self.order_product, self.description, self.return_date_time, self.is_accepted))
