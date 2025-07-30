from django.db import models
from .user import User

class UserPreferences(models.Model):
    user_preferences_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_preferences')
    dark_mode = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_preferences'

    def __str__(self):
        return "Dark_mode: " + str(self.dark_mode)

    @classmethod
    def create_user_preferences(cls, user: User):
        return cls(
            user=user,
            dark_mode=False
        )
