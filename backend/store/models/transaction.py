from django.db import models

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    buyer_id = models.IntegerField(null=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    date_time = models.DateTimeField(null=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "Total price: " + str(self.total_price)
