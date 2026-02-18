from rest_framework import serializers

from store.models import UserPreferences


class UserPreferencesOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ["dark_mode"]
