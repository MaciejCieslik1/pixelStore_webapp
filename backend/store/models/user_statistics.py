from django.db import models
from .user import User

class UserStatistics(models.Model):
    user_statistics_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_statistics')
    creation_date = models.DateField(null=False)
    products_bought = models.IntegerField(null=False)
    products_sold = models.IntegerField(null=False)

    class Meta:
        db_table = 'user_statistics'

    def __str__(self):
        return "Products bought: " + str(self.products_bought) + ", sold: " + str(self.products_sold)
