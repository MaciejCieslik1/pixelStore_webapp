from django.db import models

class UserPreferences(models.Model):
    user_preferences_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    language = models.CharField(max_length=32, null=False)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Language: " + str(self.language) + ", dark_mode: " + str(self.dark_mode)
