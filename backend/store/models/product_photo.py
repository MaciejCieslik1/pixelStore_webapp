from django.db import models

class ProductPhoto(models.Model):
    product_photo_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=False)
    image_url = models.CharField(max_length=2048, null=False)
    is_main_photo = models.BooleanField(default=False)

    def __str__(self):
        return "image_url: " + str(self.image_url)
