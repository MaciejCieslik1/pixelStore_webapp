import datetime

import pytest
from django.utils import timezone

from store.exceptions import InvalidInputData, TokenExpiredError, IncorrectTokenError, \
    TokenExpiredByReplacementError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.models import User, Contact
from store.service.contact_service import FindContactByNameService, FindAllContactsService, CreateContactService, \
    DeleteContactByNameService


@pytest.mark.django_db
class TestFindContactByNameService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token2 = AuthenticationHelper.register_and_login_user(self.user2_data)
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.objects.get(username=self.user2_data["username"])
        self.user3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token3 = AuthenticationHelper.register_and_login_user(self.user3_data)
        self.user3 = User.objects.get(username=self.user3_data["username"])
        self.service = FindContactByNameService()
        self.contact = Contact(sender=self.user1, receiver=self.user2)
        self.contact.save()
        self.contact_data = {"contact_id": self.contact.contact_id, "sender_username": self.contact.sender.username,
            "receiver_username": self.contact.receiver.username}

    def test_find_by_name_success(self):
        username = self.user2_data["username"]
        contacts_before = Contact.objects.count()
        result = self.service.find_by_name(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert result == self.contact_data
        assert contacts_after == contacts_before

    def test_find_by_name_invalid_username(self):
        username = "invalid_username"
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_name(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert "User with that username does not exist." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_by_name_not_contact_username(self):
        username = self.user3_data["username"]
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_name(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert "User with that username is not your contact." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_by_name_own_username(self):
        username = self.user_data["username"]
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_name(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert "Self username provided." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_by_name_expired_access_token(self):
        username = self.user2_data["username"]
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_by_name(access_token, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_by_name_incorrect_access_token(self):
        username = self.user2_data["username"]
        access_token = "invalid token"
        contacts_before = Contact.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_by_name(access_token, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_by_name_expired_by_replacement_access_token(self):
        username = self.user2_data["username"]
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_by_name(access_token_first, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert contacts_after == contacts_before


@pytest.mark.django_db
class TestFindAllNotificationsService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token2 = AuthenticationHelper.register_and_login_user(self.user2_data)
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.objects.get(username=self.user2_data["username"])
        self.user3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token3 = AuthenticationHelper.register_and_login_user(self.user3_data)
        self.user3 = User.objects.get(username=self.user3_data["username"])
        self.service = FindAllContactsService()
        self.contact = Contact(sender=self.user1, receiver=self.user2)
        self.contact.save()
        self.contact2 = Contact(sender=self.user1, receiver=self.user3)
        self.contact2.save()
        self.contact3 = Contact(sender=self.user2, receiver=self.user3)
        self.contact3.save()
        self.contact_data = [
            {"contact_id": self.contact.contact_id, "sender_username": self.contact.sender.username,
                "receiver_username": self.contact.receiver.username},
            {"contact_id": self.contact2.contact_id, "sender_username": self.contact2.sender.username,
                "receiver_username": self.contact2.receiver.username}]
        self.validated_data = {"page": 1, "page_size": 10}

    def test_find_all(self):
        contacts_before = Contact.objects.count()
        result = self.service.find_all(token=self.token, user=self.user1, validated_data=self.validated_data)
        contacts_after = Contact.objects.count()

        assert result == self.contact_data
        assert contacts_after == contacts_before

    def test_find_all_filter_1_page_1_page_size(self):
        self.validated_data["page_size"] = 1
        contacts_before = Contact.objects.count()
        result = self.service.find_all(token=self.token, user=self.user1, validated_data=self.validated_data)
        contacts_after = Contact.objects.count()

        assert result == self.contact_data[0]
        assert contacts_after == contacts_before

    def test_find_all_filter_1_page_2_page_size(self):
        self.validated_data["page_size"] = 2
        contacts_before = Contact.objects.count()
        result = self.service.find_all(token=self.token, user=self.user1, validated_data=self.validated_data)
        contacts_after = Contact.objects.count()

        assert result == self.contact_data
        assert contacts_after == contacts_before

    def test_find_all_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
                                                              timezone.now() - datetime.timedelta(days=1),
                                                              timezone.now() - datetime.timedelta(days=2),
                                                              token_version=1)
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_all(access_token, self.user, self.validated_data)
        contacts_after = Contact.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_all_incorrect_access_token(self):
        access_token = "invalid token"
        contacts_before = Contact.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_all(access_token, self.user, self.validated_data)
        contacts_after = Contact.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert contacts_after == contacts_before

    def test_find_all_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_all(access_token_first, self.user, self.validated_data)
        contacts_after = Contact.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert contacts_after == contacts_before


@pytest.mark.django_db
class TestCreateContactService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token2 = AuthenticationHelper.register_and_login_user(self.user2_data)
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.objects.get(username=self.user2_data["username"])
        self.user3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token3 = AuthenticationHelper.register_and_login_user(self.user3_data)
        self.user3 = User.objects.get(username=self.user3_data["username"])
        self.service = CreateContactService()
        self.creation_data = {"receiver_username": self.user2_data["username"]}

    def test_create_success(self):
        contacts_before = Contact.objects.count()
        result = self.service.create(token=self.token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert result == "Contact created successfully."
        assert contacts_after == contacts_before + 1

    def test_create_invalid_username(self):
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(token=self.token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert "User with that username does not exist." in str(e.value)
        assert contacts_after == contacts_before

    def test_create_is_already_contact(self):
        contact = Contact(self.user1, self.user2)
        contact.save()
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(token=self.token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert "User with that username is already your contact." in str(e.value)
        assert contacts_after == contacts_before

    def test_create_own_username(self):
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.create(token=self.token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert "Self username provided." in str(e.value)
        assert contacts_after == contacts_before

    def test_create_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.create(token=access_token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert contacts_after == contacts_before

    def test_create_incorrect_access_token(self):
        access_token = "invalid token"
        contacts_before = Contact.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.create(token=access_token, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert contacts_after == contacts_before

    def test_create_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.create(token=access_token_first, user=self.user1, new_contact_data=self.creation_data)
        contacts_after = Contact.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert contacts_after == contacts_before


@pytest.mark.django_db
class TestDeleteContactByNameService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token2 = AuthenticationHelper.register_and_login_user(self.user2_data)
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.objects.get(username=self.user2_data["username"])
        self.user3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        self.token3 = AuthenticationHelper.register_and_login_user(self.user3_data)
        self.user3 = User.objects.get(username=self.user3_data["username"])
        self.service = DeleteContactByNameService()
        self.contact = Contact(sender=self.user1, receiver=self.user2)
        self.contact.save()

    def test_delete_by_name_success(self):
        username = self.user2_data["username"]
        contacts_before = Contact.objects.count()
        result = self.service.delete(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert result == "Contact deleted successfully"
        assert contacts_after == contacts_before - 1

    def test_delete_name_invalid_username(self):
        username = "invalid_username"
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert "User with that username does not exist." in str(e.value)
        assert contacts_after == contacts_before

    def test_delete_by_name_not_contact_username(self):
        username = self.user3_data["username"]
        contacts_before = Contact.objects.count()

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(token=self.token, user=self.user1, username=username)
        contacts_after = Contact.objects.count()

        assert "User with that username is not your contact." in str(e.value)
        assert contacts_after == contacts_before

    def test_delete_by_name_expired_access_token(self):
        username = self.user2_data["username"]
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id, "access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.delete(access_token, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert contacts_after == contacts_before

    def test_delete_by_name_incorrect_access_token(self):
        username = self.user2_data["username"]
        access_token = "invalid token"
        contacts_before = Contact.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.delete(access_token, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert contacts_after == contacts_before

    def test_delete_by_name_expired_by_replacement_access_token(self):
        username = self.user2_data["username"]
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        self.user = User.objects.get(username="tester")
        contacts_before = Contact.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.delete(access_token_first, self.user, username)
        contacts_after = Contact.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert contacts_after == contacts_before
