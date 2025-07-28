from django.db import models
from .user import User

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    date_time = models.DateTimeField(null=False)
    is_finished = models.BooleanField(default=False)

    class Meta:
        db_table = 'transaction'
        indexes = [models.Index(fields=['date_time'])]

    def __str__(self):
        return "Total price: " + str(self.total_price)
