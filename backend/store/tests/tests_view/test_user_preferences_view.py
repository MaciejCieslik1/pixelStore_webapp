from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import IncorrectTokenError, TokenExpiredError, CannotGetTokenFromRequestError, \
    TokenExpiredByReplacementError, InvalidInputData
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user



@pytest.mark.django_db
class TestFindUserPreferences:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.find_user_preferences_data = {"dark_mode": True}

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_success(self, mock_find):
        mock_find.return_value = self.find_user_preferences_data

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.find_user_preferences_data
        mock_find.assert_called_once()

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_invalid_token(self, mock_find):
        mock_find.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_expired_token(self, mock_find):
        mock_find.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_cannot_get_token_from_request(self, mock_find):
        mock_find.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_token_expired_by_replacement(self, mock_find):
        mock_find.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.FindUserPreferencesService.find")
    def test_find_other_exception(self, mock_find):
        mock_find.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/user_preferences/find/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestUpdateUserPreferences:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.communicate = "User preferences updated successfully"
        self.user_preferences_update_data = {"dark_mode": True}

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_success(self, mock_update):
        mock_update.return_value = self.communicate

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == self.communicate
        mock_update.assert_called_once()

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_invalid_token(self, mock_update):
        mock_update.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_expired_token(self, mock_update):
        mock_update.side_effect = TokenExpiredError("Access token error.")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_cannot_get_token_from_request(self, mock_update):
        mock_update.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_token_expired_by_replacement(self, mock_update):
        mock_update.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_other_exception(self, mock_update):
        mock_update.side_effect = DatabaseError("DB connection failed")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.user_preferences_service.UpdateUserPreferencesService.update")
    def test_update_invalid_input_data(self, mock_update):
        mock_update.side_effect = InvalidInputData("Invalid input data provided.")

        response = self.client.put(f"/user_preferences/update/", data=self.user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."

    def test_update_invalid_serializer(self):
        user_preferences_update_data = {"dark_mode": 13}
        response = self.client.put(f"/user_preferences/update/", data=user_preferences_update_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
