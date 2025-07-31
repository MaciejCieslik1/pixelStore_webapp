from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=64, unique=True)
    username = models.CharField(max_length=32, unique=True)
    password_hash = models.CharField(max_length=96, null=False)
    is_verified = models.BooleanField(default=False)
    bio = models.CharField(max_length=1024, null=False)
    money = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return "Email: " + self.email

    @classmethod
    def create_user(cls, data: dict, password_hash: str):
        return cls(
            email=data["email"],
            username=data["username"],
            password_hash=password_hash,
            is_verified=False,
            bio="I'm new here!",
            money=0.00
        )
