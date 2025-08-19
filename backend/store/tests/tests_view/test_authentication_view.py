import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.db import DatabaseError

from store.exceptions import UsernameAlreadyTakenError, UserNotFoundError, InvalidPasswordError, UserNotVerifiedError, \
    TokenExpiredError, CannotGetTokenFromRequestError, InvalidVerificationCodeError, ExpiredVerificationCodeError
from store.helper_classes.authentication_helper import TokenGenerator
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User
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

    def test_verify_account_serializer_error(self):
        response = self.client.post("/verify_account/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.user_data["is_verified"] = True
        self.user = User.create_user(self.user_data)
        self.user.save()
        token = TokenGenerator.generate_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @patch("store.service.authentication_service.LogoutService.logout_user")
    def test_logout_success(self, mock_logout_user):
        mock_logout_user.return_value = "User successfully logged out."

        response = self.client.post("/logout/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "User successfully logged out."
        mock_logout_user.assert_called_once()


    @patch("store.service.authentication_service.LogoutService.logout_user")
    def test_logout_token_expired(self, mock_logout_user):
        mock_logout_user.side_effect = TokenExpiredError("Invalid token.")

        response = self.client.post("/logout/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.LogoutService.logout_user")
    def test_logout_cannot_get_token_from_request(self, mock_logout_user):
        mock_logout_user.side_effect = CannotGetTokenFromRequestError("Connot get token.")

        response = self.client.post("/logout/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.LogoutService.logout_user")
    def test_login_other_exception(self, mock_logout_user):
        mock_logout_user.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/logout/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestVerifyAccountView:
    def setup_method(self):
        self.client = APIClient()
        self.data = {"email": "test@example.com", "verification_code": "ABCDEabcd1"}

    @patch("store.service.authentication_service.VerifyAccountService.verify_account")
    def test_verify_account_success(self, mock_verify_account):
        mock_verify_account.return_value = {"msg": "Account successfully verified."}

        response = self.client.post("/verify_account/", self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Account successfully verified."
        mock_verify_account.assert_called_once_with(self.data)

    @patch("store.service.authentication_service.VerifyAccountService.verify_account")
    def test_verify_account_invalid_verification_code(self, mock_verify_account):
        mock_verify_account.side_effect = InvalidVerificationCodeError("Invalid verification code.")

        response = self.client.post("/verify_account/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Verification code error."

    @patch("store.service.authentication_service.VerifyAccountService.verify_account")
    def test_verify_account_expired_verification_code(self, mock_verify_account):
        mock_verify_account.side_effect = ExpiredVerificationCodeError("Verification ncode has expired.")

        response = self.client.post("/verify_account/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Verification code error."

    @patch("store.service.authentication_service.VerifyAccountService.verify_account")
    def test_verify_account_other_exception(self, mock_verify_account):
        mock_verify_account.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/verify_account/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_verify_account_serializer_error(self):
        response = self.client.post("/verify_account/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
