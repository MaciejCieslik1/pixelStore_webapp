from rest_framework import serializers

from store.models import Notification

class NotificationOutputSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username")

    class Meta:
        model = Notification
        fields = ["notification_id", "sender_username", "sent_date_time", "text"]
