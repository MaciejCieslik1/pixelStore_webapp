from django.db import models
from django.conf import settings

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return "Sender: " + str(self.sender.id) + ", receiver: " + str(self.receiver.id)

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return NotImplemented
        return self.sender == other.sender and self.receiver == other.receiver

    def __hash__(self):
        return hash((self.sender, self.receiver))
