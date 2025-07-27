from django.db import models

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField(null=False)
    receiver_id = models.IntegerField(null=False)
    sent_date_time = models.DateTimeField(null=False)
    text = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "Notification text: " + self.text
