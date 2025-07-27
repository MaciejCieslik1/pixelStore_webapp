from django.db import models

class OrderReturn(models.Model):
    order_return_id = models.AutoField(primary_key=True)
    ordered_product_id = models.IntegerField(null=False)
    description = models.CharField(max_length=1024, null=False)
    return_date_time = models.DateTimeField(null=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return "description: " + str(self.description)
