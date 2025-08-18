import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.db import DatabaseError

from store.exceptions import UsernameAlreadyTakenError, UserNotFoundError, InvalidPasswordError, UserNotVerifiedError
from store.service.authentication_service import EmailAlreadyTakenError


@pytest.mark.django_db
class TestRegisterView:
    def setup_method(self):
        self.client = APIClient()
        self.data = {"email": "test@example.com", "username": "tester", "password": "Abcdefg1#abc",
                "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

    @patch("store.service.authentication_service.RegisterService.register_user")
    def test_register_success(self, mock_register_user):
        mock_register_user.return_value = "User tester registered successfully."

        response = self.client.post("/register/", self.data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["msg"] == "User tester registered successfully."
        mock_register_user.assert_called_once_with(self.data)

    def test_register_invalid_serializer(self):
        self.data["password"] = ""
        self.data["email"] = ""
        response = self.client.post("/register/", self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    @patch("store.service.authentication_service.RegisterService.register_user")
    def test_register_email_already_taken(self, mock_register_user):
        mock_register_user.side_effect = EmailAlreadyTakenError("Email is already taken")

        response = self.client.post("/register/", self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Validation error"

    @patch("store.service.authentication_service.RegisterService.register_user")
    def test_register_username_already_taken(self, mock_register_user):
        mock_register_user.side_effect = UsernameAlreadyTakenError("Username is already taken")

        response = self.client.post("/register/", self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Validation error"

    @patch("store.service.authentication_service.RegisterService.register_user")
    def test_register_database_error(self, mock_register_user):
        mock_register_user.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/register/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Database error occurred."
        assert response.data["details"] == "DB connection failed"


@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.client = APIClient()
        self.data = {"email": "test@example.com", "password": "Abcdefg1#abc"}

    @patch("store.service.authentication_service.LoginService.login_user")
    def test_login_success(self, mock_login_user):
        mock_login_user.return_value = {"msg": "User successfully logged in.", "access_token": "access_token",
                                        "refresh_token": "refresh_token"}

        response = self.client.post("/login/", self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "User successfully logged in."
        assert response.data["access_token"] == "access_token"
        assert response.data["refresh_token"] == "refresh_token"
        mock_login_user.assert_called_once_with(self.data)

    @patch("store.service.authentication_service.LoginService.login_user")
    def test_login_user_not_found(self, mock_login_user):
        mock_login_user.side_effect = UserNotFoundError("No user given.")

        response = self.client.post("/login/", self.data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    @patch("store.service.authentication_service.LoginService.login_user")
    def test_login_invalid_password(self, mock_login_user):
        mock_login_user.side_effect = InvalidPasswordError("Incorrect password.")

        response = self.client.post("/login/", self.data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"] == "Invalid credentials."

    @patch("store.service.authentication_service.LoginService.login_user")
    def test_login_user_not_verified(self, mock_login_user):
        mock_login_user.side_effect = UserNotVerifiedError("User not verified.")

        response = self.client.post("/login/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Validation error."

    @patch("store.service.authentication_service.LoginService.login_user")
    def test_login_other_exception(self, mock_login_user):
        mock_login_user.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/login/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."
