from datetime import datetime
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
        self.find_user_statistics_data = {"creation_date": datetime.now().isoformat().replace("+00:00", "Z"),
                                          "products_bought": 1, "products_sold": 2}
        self.username = self.user.username

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_success(self, mock_find):
        mock_find.return_value = self.find_user_statistics_data

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.find_user_statistics_data
        mock_find.assert_called_once()

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_invalid_token(self, mock_find):
        mock_find.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_expired_token(self, mock_find):
        mock_find.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_cannot_get_token_from_request(self, mock_find):
        mock_find.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_token_expired_by_replacement(self, mock_find):
        mock_find.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_other_exception(self, mock_find):
        mock_find.side_effect = DatabaseError("DB connection failed")

        response = self.client.get(f"/user_statistics/find_by_username/{self.username}/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    @patch("store.service.user_statistics_service.FindByUsernameUserStatisticsService.find_by_username")
    def test_find_by_username_invalid_input_data(self, mock_find_by_username):
        mock_find_by_username.side_effect = InvalidInputData("Invalid input data provided.")
        username = 12

        response = self.client.get(f"/user_statistics/find_by_username/{username}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid input data provided."
