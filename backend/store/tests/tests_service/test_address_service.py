from datetime import timedelta

import pytest
from django.utils import timezone

from store.exceptions import TokenExpiredError, IncorrectTokenError, TokenExpiredByReplacementError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.models import User, Address
from store.service.address_service import FindAddressService, UpdateAddressService


@pytest.mark.django_db
class TestFindAddressService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.address_data = {"address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.user = User.objects.get(username="tester")
        self.service = FindAddressService()

    def test_find_address(self):
        address_count_before = Address.objects.count()
        result = self.service.find(self.token, self.user)
        address_count_after = Address.objects.count()

        assert self.address_data == result
        assert address_count_after == address_count_before

    def test_find_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        address_count_before = Address.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find(access_token, self.user)
        address_count_after = Address.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert address_count_after == address_count_before

    def test_find_incorrect_access_token(self):
        access_token = "invalid token"

        address_count_before = Address.objects.count()
        with pytest.raises(IncorrectTokenError) as e:
            self.service.find(access_token, self.user)
        address_count_after = Address.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert address_count_after == address_count_before

    def test_find_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        address_count_before = Address.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find(access_token_first, user)
        address_count_after = Address.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert address_count_after == address_count_before


@pytest.mark.django_db
class TestUpdateAddressService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.address_data = {"address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.new_address_data = {"address": "sddsdsd", "postal_code": "00002", "city": "London", "country": "UK"}
        self.user = User.objects.get(username="tester")
        self.service = UpdateAddressService()

    def test_update_address(self):
        address_count_before = Address.objects.count()
        result = self.service.update(self.token, self.user, self.new_address_data)
        address_count_after = Address.objects.count()

        assert address_count_after == address_count_before
        assert result == "Address successfully updated."

    def test_update_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        address_count_before = Address.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.update(access_token, self.user, self.new_address_data)
        address_count_after = Address.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert address_count_after == address_count_before

    def test_update_incorrect_access_token(self):
        access_token = "invalid token"
        address_count_before = Address.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.update(access_token, self.user, self.new_address_data)
        address_count_after = Address.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert address_count_after == address_count_before

    def test_update_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        address_count_before = Address.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.update(access_token_first, user, self.new_address_data)
        address_count_after = Address.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert address_count_after == address_count_before
