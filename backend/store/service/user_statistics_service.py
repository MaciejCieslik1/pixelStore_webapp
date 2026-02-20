from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, UserStatistics
from store.output_serializers.user_statistic_output_serializer import UserStatisticsOutputSerializer


class FindByUsernameUserStatisticsService:
    def find_by_username(self, token: str, user: User, username: str) -> dict:
        TokenUtils.verify_access_token(token, user)

        user = User.objects.filter(username=username).first()
        if user is None:
            raise InvalidInputData("User with this username does not exist.")

        user_statistics = UserStatistics.objects.filter(user=user).first()

        serializer = UserStatisticsOutputSerializer(user_statistics)
        return serializer.data

