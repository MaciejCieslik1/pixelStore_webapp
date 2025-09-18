import datetime

import pytest
from django.utils import timezone

from store.exceptions import TokenExpiredError, IncorrectTokenError, TokenExpiredByReplacementError, \
    InvalidUsernameError, SelfUsernameError, InvalidNotificationIdError, NotificationIdDoesNotBelongToUserError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.models import User, Notification
from store.service.notification_service import FindAllNotificationsService, CreateNotificationService, \
    DeleteNotificationService


@pytest.mark.django_db
class TestFindAllNotificationsService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
             "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
             "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.create_user(self.user2_data)
        self.user2.save()
        sender_id = self.user2.user_id
        receiver_id = self.user1.user_id
        self.date = timezone.now()
        self.yesterday = self.date - datetime.timedelta(days=1)
        self.notification1 = Notification(sender_id=sender_id, receiver_id=receiver_id, sent_date_time=self.date, text="notification1")
        self.notification2 = Notification(sender_id=sender_id, receiver_id=receiver_id, sent_date_time=self.date, text="notification2")
        self.notification3 = Notification(sender_id=sender_id, receiver_id=receiver_id, sent_date_time=self.yesterday, text="notification3")
        self.notification1.save()
        self.notification2.save()
        self.notification3.save()
        self.notifications_data = [{"notification_id": self.notification1.notification_id, "sender_username": "tester2",
            "sent_date_time": self.date.isoformat().replace("+00:00", "Z"), "text": "notification1"},
            {"notification_id": self.notification2.notification_id,"sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
                "text": "notification2"},
            {"notification_id": self.notification3.notification_id, "sender_username": "tester2", "sent_date_time": self.yesterday.isoformat().replace("+00:00", "Z"),
                "text": "notification3"}]
        self.data = {"date_from": None, "date_to": None, "order": "desc", "page": 1, "page_size": 10}
        self.service = FindAllNotificationsService()

    def test_find_all_no_filters(self):
        notifications_before = Notification.objects.count()

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_order_asc(self):
        notifications_before = Notification.objects.count()
        self.data["order"] = "asc"
        self.notifications_data = [{"notification_id": self.notification3.notification_id, "sender_username": "tester2",
            "sent_date_time": self.yesterday.isoformat().replace("+00:00", "Z"), "text": "notification3"},
            {"notification_id": self.notification1.notification_id, "sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
             "text": "notification1"},
            {"notification_id": self.notification2.notification_id, "sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
             "text": "notification2"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_0_dates(self):
        notifications_before = Notification.objects.count()
        self.data["date_to"] = (self.date - datetime.timedelta(days=2)).isoformat().replace("+00:00", "Z")
        self.notifications_data = []

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_1_date(self):
        notifications_before = Notification.objects.count()
        self.data["date_from"] = (self.date - datetime.timedelta(days=1)).isoformat().replace("+00:00", "Z")
        self.data["date_to"] = (self.date - datetime.timedelta(days=1)).isoformat().replace("+00:00", "Z")
        self.notifications_data = [{"notification_id": self.notification3.notification_id, "sender_username": "tester2", "sent_date_time": self.yesterday.isoformat().replace("+00:00", "Z"), "text": "notification3"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_2_dates(self):
        notifications_before = Notification.objects.count()
        self.data["date_from"] = self.date.isoformat().replace("+00:00", "Z")
        self.data["date_to"] = self.date.isoformat().replace("+00:00", "Z")
        self.notifications_data = [{"notification_id": self.notification1.notification_id, "sender_username": "tester2",
            "sent_date_time": self.date.isoformat().replace("+00:00", "Z"), "text": "notification1"},
            {"notification_id": self.notification2.notification_id, "sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
            "text": "notification2"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_3_dates(self):
        notifications_before = Notification.objects.count()
        self.data["date_from"] = self.yesterday.isoformat().replace("+00:00", "Z")
        self.data["date_to"] = self.date.isoformat().replace("+00:00", "Z")
        self.notifications_data = [{"notification_id": self.notification1.notification_id, "sender_username": "tester2",
            "sent_date_time": self.date.isoformat().replace("+00:00", "Z"), "text": "notification1"},
            {"notification_id": self.notification2.notification_id, "sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
            "text": "notification2"},
            {"notification_id": self.notification3.notification_id, "sender_username": "tester2", "sent_date_time": self.yesterday.isoformat().replace("+00:00", "Z"),
             "text": "notification3"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_1_page_1_page_size(self):
        notifications_before = Notification.objects.count()
        self.data["page_size"] = 1
        self.notifications_data = [{"notification_id": self.notification1.notification_id, "sender_username": "tester2",
            "sent_date_time": self.date.isoformat().replace("+00:00", "Z"), "text": "notification1"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_filter_1_page_2_page_size_asc(self):
        notifications_before = Notification.objects.count()
        self.data["page_size"] = 2
        self.data["order"] = "asc"
        self.notifications_data = [{"notification_id": self.notification3.notification_id,
            "sender_username": "tester2", "sent_date_time": self.yesterday.isoformat().replace("+00:00", "Z"), "text": "notification3"},
        {"notification_id": self.notification1.notification_id, "sender_username": "tester2", "sent_date_time": self.date.isoformat().replace("+00:00", "Z"),
        "text": "notification1"}]

        result = self.service.find_all(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert self.notifications_data == result
        assert notifications_after == notifications_before

    def test_find_all_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user1.user_id,"access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_all(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert notifications_before == notifications_after

    def test_find_all_incorrect_access_token(self):
        access_token = "invalid token"
        notifications_before = Notification.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_all(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert notifications_before == notifications_after

    def test_find_all_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_all(access_token_first, user, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert notifications_before == notifications_after


@pytest.mark.django_db
class TestCreateNotificationService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
             "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
             "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.user2 = User.create_user(self.user2_data)
        self.user2.save()
        self.data = {"username": "tester2", "date": timezone.now(), "text": "Hello"}
        self.service = CreateNotificationService()

    def test_create_notification(self):
        notifications_before = Notification.objects.count()

        result = self.service.create(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert result == "Notification created successfully."
        assert notifications_after == notifications_before + 1

    def test_create_invalid_username(self):
        notifications_before = Notification.objects.count()
        self.data["username"] = "invalid_username"

        with pytest.raises(InvalidUsernameError) as e:
            self.service.create(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Invalid username of a notification receiver." in str(e.value)
        assert notifications_before == notifications_after
        
    def test_create_invalid_username_self_username(self):
        notifications_before = Notification.objects.count()
        self.data["username"] = "tester"

        with pytest.raises(SelfUsernameError) as e:
            self.service.create(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Self username provided." in str(e.value)
        assert notifications_before == notifications_after

    def test_create_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user1.user_id,"access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.create(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert notifications_before == notifications_after

    def test_create_incorrect_access_token(self):
        access_token = "invalid token"
        notifications_before = Notification.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.create(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert notifications_before == notifications_after

    def test_create_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.create(access_token_first, user, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert notifications_before == notifications_after


@pytest.mark.django_db
class TestDeleteNotificationService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
             "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
             "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.user1 = User.objects.get(username=self.user_data["username"])
        self.token2 = AuthenticationHelper.register_and_login_user(self.user2_data)
        self.user2 = User.objects.get(username=self.user2_data["username"])
        sender_id = self.user1.user_id
        receiver_id = self.user2.user_id
        self.date = timezone.now()
        self.yesterday = self.date - datetime.timedelta(days=1)
        notification1 = Notification(sender_id=sender_id, receiver_id=receiver_id, sent_date_time=self.date,
                                     text="notification1")
        notification1.save()
        notification_id = notification1.notification_id
        self.data = {"notification_id": notification_id}
        self.service = DeleteNotificationService()

    def test_delete_notification(self):
        notifications_before = Notification.objects.count()

        result = self.service.delete(self.token, self.user2, self.data)
        notifications_after = Notification.objects.count()

        assert result == "Notification deleted successfully."
        assert notifications_after == notifications_before - 1

    def test_delete_notification_invalid_id(self):
        notifications_before = Notification.objects.count()
        self.data["notification_id"] = self.data["notification_id"] + 1

        with pytest.raises(InvalidNotificationIdError) as e:
            self.service.delete(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Invalid notification id." in str(e.value)
        assert notifications_after == notifications_before

    def test_delete_notification_id_does_not_belong_to_user(self):
        user3_data = {"email": "test3@example.com", "username": "tester3", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        user3 = User.create_user(user3_data)
        user3.save()
        user4_data = {"email": "test4@example.com", "username": "tester4", "password": "Abc123#ab",
                      "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                      "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                      "country": "Poland"}
        user4 = User.create_user(user4_data)
        user4.save()
        sender_id = user3.user_id
        receiver_id = user4.user_id
        self.date = timezone.now()
        self.yesterday = self.date - datetime.timedelta(days=1)
        notification = Notification(sender_id=sender_id, receiver_id=receiver_id, sent_date_time=self.date,
                                     text="notification")
        notification.save()
        notifications_before = Notification.objects.count()
        self.data["notification_id"] = notification.notification_id

        with pytest.raises(NotificationIdDoesNotBelongToUserError) as e:
            self.service.delete(self.token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert "Notification with given id does not belong to the user." in str(e.value)
        assert notifications_after == notifications_before

    def test_delete_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user1.user_id,"access",
            timezone.now() - datetime.timedelta(days=1), timezone.now() - datetime.timedelta(days=2), token_version=1)
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.delete(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert notifications_before == notifications_after

    def test_delete_incorrect_access_token(self):
        access_token = "invalid token"
        notifications_before = Notification.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.delete(access_token, self.user1, self.data)
        notifications_after = Notification.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert notifications_before == notifications_after

    def test_delete_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        notifications_before = Notification.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.delete(access_token_first, user, self.data)
        notifications_after = Notification.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert notifications_before == notifications_after
