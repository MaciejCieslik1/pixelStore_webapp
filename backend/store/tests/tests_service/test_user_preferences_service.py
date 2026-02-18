import pytest
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User, UserPreferences
from store.service.user_preferences_service import FindUserPreferencesService, UpdateUserPreferencesService


@pytest.mark.django_db
class TestFindService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.service = FindUserPreferencesService()
        self.result = {"dark_mode": False}


    def test_find(self):
        user_preferences_before = UserPreferences.objects.all().count()
        result = self.service.find(self.token, self.owner)
        user_preferences_after = UserPreferences.objects.all().count()

        assert result == self.result
        assert user_preferences_before == user_preferences_after


@pytest.mark.django_db
class TestUpdateService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_preferences_update_data = {"dark_mode": True}
        self.service = UpdateUserPreferencesService()
        self.communicate = "User preferences updated successfully."


    def test_update(self):
        user_preferences_before = UserPreferences.objects.all().count()
        result = self.service.update(self.token, self.owner, self.user_preferences_update_data)
        user_preferences_after = UserPreferences.objects.all().count()
        user_preferences = UserPreferences.objects.filter(user_id=self.owner.user_id).first()

        assert result == self.communicate
        assert user_preferences_before == user_preferences_after
        assert user_preferences.dark_mode == True
