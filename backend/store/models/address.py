from django.conf import settings
from django.db import models
from .user import User


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')
    address = models.CharField(max_length=64, null=False)
    postal_code = models.CharField(max_length=5, null=False)
    city = models.CharField(max_length=32, null=False)
    country = models.CharField(max_length=32, null=False)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return "Address: " + self.address

    @classmethod
    def create_address(cls, data: dict, user: User):
        return cls(
            user=user,
            address=data["address"],
            postal_code=data["postal_code"],
            city=data["city"],
            country=data["country"]
        )

    def __eq__(self, other):
        if not isinstance(other, Address):
            return NotImplemented
        return (self.user == other.user and self.address == other.address and self.postal_code == other.postal_code
            and self.city == other.city and self.country == other.country)

    def __hash__(self):
        return hash((self.user, self.address, self.postal_code, self.city, self.country))
