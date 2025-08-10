from datetime import date
from django.conf import settings
from django.db import models
from .user import User

class UserStatistics(models.Model):
    user_statistics_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_statistics')
    creation_date = models.DateField(null=False)
    products_bought = models.IntegerField(null=False)
    products_sold = models.IntegerField(null=False)

    class Meta:
        db_table = 'user_statistics'

    def __str__(self):
        return "Products bought: " + str(self.products_bought) + ", sold: " + str(self.products_sold)

    @classmethod
    def create_user_statistics(cls, user: User):
        return cls(
            user=user,
            creation_date=date.today(),
            products_bought=0,
            products_sold=0
        )

    def __eq__(self, other):
        if not isinstance(other, UserStatistics):
            return NotImplemented
        return (self.user == other.user and self.creation_date == other.creation_date and
            self.products_bought == other.products_bought and self.products_sold == other.products_sold)

    def __hash__(self):
        return hash((self.user, self.creation_date, self.products_bought, self.products_sold))
