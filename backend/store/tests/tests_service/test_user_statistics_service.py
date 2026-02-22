from datetime import datetime

import pytest

from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User, UserStatistics
from store.service.user_statistics_service import FindByUsernameUserStatisticsService


@pytest.mark.django_db
class TestFindByUsernameService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["username"] = "tester10"
        self.user_data2["email"] = "test10@example.com"
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.user2 = User.objects.get(username=self.user_data2["username"])
        creation_date = UserStatistics.objects.filter(user=self.user2).first().creation_date
        self.service = FindByUsernameUserStatisticsService()
        self.result = {"username": self.user2.username, "creation_date": creation_date.isoformat(), "products_bought": 0, "products_sold": 0}


    def test_find_by_username(self):
        user_before = UserStatistics.objects.all().count()
        result = self.service.find_by_username(self.token, self.owner, self.user2.username)
        users_after = UserStatistics.objects.all().count()

        assert result == self.result
        assert user_before == users_after


    def test_find_by_username_user_not_exist(self):
        user_statistics_before = UserStatistics.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_username(self.token, self.owner, "bad username")
        user_statistics_after = UserStatistics.objects.all().count()

        assert f"User with this username does not exist." in str(e.value)
        assert user_statistics_before == user_statistics_after
