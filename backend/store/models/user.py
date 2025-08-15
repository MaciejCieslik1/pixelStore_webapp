from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)  # This is password hash but Django requires 'password' column name
    is_verified = models.BooleanField(default=False)
    bio = models.CharField(max_length=1024, default="I'm new here!")
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_superuser = models.BooleanField(default=False) # Field required by Django
    last_login = models.DateTimeField(blank=True, null=True) # Field required by Django
    token_version = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = models.Manager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"Email: {self.email}"

    @classmethod
    def create_user(cls, data: dict):
        user = cls(
            email=data["email"],
            username=data["username"],
            is_verified=False,
            bio="I'm new here!",
            money=0.00
        )
        user.set_password(data["password"])
        return user

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return (self.email == other.email and self.username == other.username and self.password == other.password
            and self.is_verified == other.is_verified and self.bio == other.bio and self.money == other.money
            and self.is_superuser == other.is_superuser and self.last_login == other.last_login
            and self.token_version == other.token_version)

    def __hash__(self):
        return hash((self.email, self.username, self.password, self.is_verified, self.bio, self.money,
            self.is_superuser, self.last_login, self.token_version))
