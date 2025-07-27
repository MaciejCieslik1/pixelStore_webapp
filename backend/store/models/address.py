from django.db import models

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    address = models.CharField(max_length=64, null=False)
    postal_code = models.CharField(max_length=5, null=False)
    city = models.CharField(max_length=32, null=False)
    country = models.CharField(max_length=32, null=False)

    def __str__(self):
        return "Address: " + self.address
