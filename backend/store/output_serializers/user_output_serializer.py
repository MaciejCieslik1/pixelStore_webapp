from rest_framework import serializers

from store.models import User


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "bio", "money"]
