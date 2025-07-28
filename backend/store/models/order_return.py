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
