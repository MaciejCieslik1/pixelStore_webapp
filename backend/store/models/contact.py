from django.db import models

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField(null=False)
    receiver_id = models.IntegerField(null=False)

    def __str__(self):
        return "Sender: " + str(self.sender_id) + ", receiver: " + str(self.receiver_id)