from django.db import models

class VerificationCode(models.Model):
    verification_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    code = models.CharField(max_length=10, null=False)
    expiration_date_time = models.DateTimeField(null=False)
    is_email_verification = models.BooleanField(default=True)

    def __str__(self):
        return "Code: " + str(self.code)