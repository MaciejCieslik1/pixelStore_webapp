from django.db import models
from django.conf import settings

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='received_notifications')
    sent_date_time = models.DateTimeField(null=False)
    text = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'notification'
        indexes = [models.Index(fields=['sent_date_time'])]

    def __str__(self):
        return "Notification text: " + self.text

    def __eq__(self, other):
        if not isinstance(other, Notification):
            return NotImplemented
        return (self.sender == other.sender and self.receiver == other.receiver and
            self.sent_date_time == other.sent_date_time and self.text == other.text)

    def __hash__(self):
        return hash((self.sender, self.receiver, self.sent_date_time, self.text))

