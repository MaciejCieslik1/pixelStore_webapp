from django.db import models
from .user import User

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return "Sender: " + str(self.sender.id) + ", receiver: " + str(self.receiver.id)
