from decimal import Decimal

import pytest
from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User, Transaction
from store.service.user_service import FindByUsernameUserService, UpdateUserService, DeleteAccountUserService


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
        self.service = FindByUsernameUserService()
        self.result = {"username": "tester10", "bio": "I'm new here!"}


    def test_find_by_username(self):
        user_before = User.objects.all().count()
        result = self.service.find_by_username(self.token, self.owner, self.user2.username)
        users_after = User.objects.all().count()

        assert result == self.result
        assert user_before == users_after


    def test_find_by_username_user_not_exist(self):
        user_before = Transaction.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_username(self.token, self.owner, "bad username")
        user_after = Transaction.objects.all().count()

        assert f"User with this username does not exist." in str(e.value)
        assert user_before == user_after


@pytest.mark.django_db
class TestUpdateUserService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user_update_data = {"money": "1000.00", "bio": "New bio!"}
        self.service = UpdateUserService()
        self.communicate = "User data updated successfully."


    def test_update_user(self):
        update_before = User.objects.all().count()
        result = self.service.update(self.token, self.owner, self.user_update_data)
        update_after = User.objects.all().count()
        owner = User.objects.get(username=self.user_data["username"])

        assert result == self.communicate
        assert owner.money == Decimal("1000.00")
        assert owner.bio == "New bio!"
        assert update_before == update_after


@pytest.mark.django_db
class TestDeleteUserService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.delete_communicate = "Deleted account successfully."
        self.service = DeleteAccountUserService()


    def test_delete(self):
        users_before = User.objects.all().count()
        result = self.service.delete(self.token, self.owner)
        users_after = User.objects.all().count()

        assert result == self.delete_communicate
        assert users_before == users_after + 1
