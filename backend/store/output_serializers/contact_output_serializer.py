from rest_framework import serializers

from store.models import Contact


class ContactOutputSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username")
    receiver_username = serializers.CharField(source="receiver.username")

    class Meta:
        model = Contact
        fields = ["contact_id", "sender_username", "receiver_username"]
