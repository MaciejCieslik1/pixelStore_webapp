from django.db import models
from .user import User
from ..requests.CreateUserRequest import CreateUserRequest


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
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
