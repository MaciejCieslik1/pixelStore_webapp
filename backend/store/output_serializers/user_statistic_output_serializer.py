from rest_framework import serializers

from store.models import UserStatistics


class UserStatisticsOutputSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = UserStatistics
        fields = ["username", "creation_date", "products_bought", "products_sold"]
