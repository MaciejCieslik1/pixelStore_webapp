from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User


class FindUserPreferencesService:
    def find(self, token: str, user: User) -> dict:
        pass


class UpdateUserPreferencesService:
    def update(self, token: str, user: User, new_user_preferences: dict) -> dict:
        pass
