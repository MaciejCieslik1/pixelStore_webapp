from django.conf import settings
from django.db import models
from .user import User
from django.utils import timezone
from datetime import timedelta
import string
import random

class VerificationCode(models.Model):
    verification_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=10, null=False)
    creation_date_time = models.DateTimeField(null=False)
    expiration_date_time = models.DateTimeField(null=False)

    class Meta:
        db_table = 'verification_code'

    def __str__(self):
        return "Code: " + str(self.code)

    @classmethod
    def create_verification_code(cls, user: User, length: int = 10):
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choices(characters, k=length))

        return cls(
            user=user,
            code=code,
            creation_date_time=timezone.now(),
            expiration_date_time=timezone.now() + timedelta(minutes=15)
        )
