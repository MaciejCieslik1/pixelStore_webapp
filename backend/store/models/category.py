from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, unique=True)
    description = models.CharField(max_length=1024, null=False)

    def __str__(self):
        return "Name: " + self.name