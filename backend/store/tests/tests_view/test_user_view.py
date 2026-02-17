from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user



@pytest.mark.django_db
class TestFindByUsernameUser:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.find_user_data = {"username": "tester2", "bio": "new bio"}

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_success(self, mock_find_by_username):
        mock_find_by_username.return_value = self.find_user_data

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.find_user_data
        mock_find_by_username.assert_called_once()

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_invalid_token(self, mock_find_by_username):
        mock_find_by_username.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_expired_token(self, mock_find_by_username):
        mock_find_by_username.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_cannot_get_token_from_request(self, mock_find_by_username):
        mock_find_by_username.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_token_expired_by_replacement(self, mock_find_by_username):
        mock_find_by_username.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_other_exception(self, mock_find_by_username):
        mock_find_by_username.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.user_service.FindByUsernameUserService.find_by_username")
    def test_find_by_username_invalid_input_data(self, mock_find_by_username):
        mock_find_by_username.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.get(f"/user/find_by_username/{self.user.username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."


@pytest.mark.django_db
class TestUpdateUser:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.communicate = "User updated successfully"
        self.user_update_data = {"money": "1000.00", "bio": "new bio"}

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_success(self, mock_update):
        mock_update.return_value = self.communicate

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.communicate
        mock_update.assert_called_once()

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.user_service.UpdateUserService.update")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.put(f"/user/update/", data=self.user_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        user_update_data = {"money": "example", "bio": "new bio"}
        response = self.client.put(f"/user/update/", data=user_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteAccountUser:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.communicate = "User's account deleted successfully"

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_success(self, mock_delete):
        mock_delete.return_value = self.communicate

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.communicate
        mock_delete.assert_called_once()

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_invalid_token(self, mock_delete):
        mock_delete.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_expired_token(self, mock_delete):
        mock_delete.side_effect = TokenExpiredError("Access token error.")

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_cannot_get_token_from_request(self, mock_delete):
        mock_delete.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_token_expired_by_replacement(self, mock_delete):
        mock_delete.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_service.DeleteAccountUserService.delete")
    def test_delete_other_exception(self, mock_delete):
        mock_delete.side_effect = DatabaseError("DB connection failed")

        response = self.client.delete(f"/user/delete_account/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."
