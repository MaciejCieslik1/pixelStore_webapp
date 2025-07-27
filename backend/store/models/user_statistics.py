from django.db import models

class UserStatistics(models.Model):
    user_statistics_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    creation_date = models.DateField(null=False)
    products_bought = models.IntegerField(null=False)
    products_sold = models.IntegerField(null=False)

    def __str__(self):
        return "Products bought: " + str(self.products_bought) + ", sold: " + str(self.products_sold)
