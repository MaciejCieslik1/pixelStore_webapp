from django.db import models
from .user import User

class VerificationCode(models.Model):
    verification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=10, null=False)
    expiration_date_time = models.DateTimeField(null=False)
    is_email_verification = models.BooleanField(default=True)

    class Meta:
        db_table = 'verification_code'

    def __str__(self):
        return "Code: " + str(self.code)