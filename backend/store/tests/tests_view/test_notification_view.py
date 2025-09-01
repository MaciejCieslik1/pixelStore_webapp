from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredByReplacementError, CannotGetTokenFromRequestError, TokenExpiredError, \
    IncorrectTokenError, UserNotFoundError, NotificationNotFoundError, NotificationNotBelongToUserError
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user


@pytest.mark.django_db
class TestFindAllNotifications:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()


    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_success(self, mock_find_all):
        mock_find_all.return_value = [{"sender_username": "tester2", "sent_date_time": "2025-08-31T12:00:00Z",
                                        "text": "Hello"}]

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["sender_username"] == "tester2"
        assert response.data[0]["sent_date_time"] == "2025-08-31T12:00:00Z"
        assert response.data[0]["text"] == "Hello"
        mock_find_all.assert_called_once()

    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_invalid_token(self, mock_find_all):
        mock_find_all.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_expired_token(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_cannot_get_token_from_request(self, mock_find_all):
        mock_find_all.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_token_expired_by_replacement(self, mock_find_all):
        mock_find_all.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.FindAllNotificationsService.find_all")
    def test_find_all_other_exception(self, mock_find_all):
        mock_find_all.side_effect = DatabaseError("DB connection failed")

        response = self.client.get("/notification/find_all/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestCreateNotification:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.data = {"sender_id": 1, "receiver_id": 2, "sent_date_time": "2025-08-31T12:00:00Z", "text": "Hello Bob!"}

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_success(self, mock_create):
        mock_create.return_value = "Notification created successfully."

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Notification created successfully."
        mock_create.assert_called_once()

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_invalid_token(self, mock_create):
        mock_create.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_expired_token(self, mock_create):
        mock_create.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_cannot_get_token_from_request(self, mock_create):
        mock_create.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_token_expired_by_replacement(self, mock_create):
        mock_create.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_user_not_found(self, mock_create):
        mock_create.side_effect = UserNotFoundError("User not found.")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    @patch("store.service.notification_service.CreateNotificationService.create")
    def test_create_other_exception(self, mock_create):
        mock_create.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/notification/create/", data=self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestDeleteNotification:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.data = {"notification_id": 1}

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = "Notification deleted successfully."

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Notification deleted successfully."
        mock_delete.assert_called_once()

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_notification_not_found(self, mock_delete):
        mock_delete.side_effect = NotificationNotFoundError("Notification not found.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Notification not found."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_notification_not_belong_to_user(self, mock_delete):
        mock_delete.side_effect = NotificationNotBelongToUserError("Notification does not belong to the user.")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Notification does not belong to the user."

    @patch("store.service.notification_service.DeleteNotificationService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete("/notification/delete/", data=self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

