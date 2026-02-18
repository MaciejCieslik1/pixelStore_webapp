from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, UserPreferences
from store.output_serializers.user_preferences_output_serializer import UserPreferencesOutputSerializer


class FindUserPreferencesService:
    def find(self, token: str, user: User) -> dict:
        TokenUtils.verify_access_token(token, user)

        user_preferences = UserPreferences.objects.filter(user_id=user.user_id).first()

        serializer = UserPreferencesOutputSerializer(user_preferences)
        return serializer.data


class UpdateUserPreferencesService:
    def update(self, token: str, user: User, new_user_preferences: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        user_preferences = UserPreferences.objects.filter(user_id=user.user_id).first()

        user_preferences.dark_mode = new_user_preferences["dark_mode"]
        user_preferences.save()

        return "User preferences updated successfully."
