from django.conf import settings
from django.db import models


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='transactions')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    date_time = models.DateTimeField(null=False)
    is_finished = models.BooleanField(default=False)

    class Meta:
        db_table = 'transaction'
        indexes = [models.Index(fields=['date_time'])]

    def __str__(self):
        return "Total price: " + str(self.total_price)

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented
        return (self.buyer == other.buyer and self.total_price == other.total_price and
            self.date_time == other.date_time and self.is_finished == other.is_finished)

    def __hash__(self):
        return hash((self.buyer, self.total_price, self.date_time, self.is_finished))
