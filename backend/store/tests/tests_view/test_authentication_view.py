import jwt
import pytest
from unittest.mock import patch, ANY
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.db import DatabaseError

from store.exceptions import UsernameAlreadyTakenError, UserNotFoundError, InvalidPasswordError, UserNotVerifiedError, \
    TokenExpiredError, CannotGetTokenFromRequestError, InvalidVerificationCodeError, ExpiredVerificationCodeError, \
    RefreshTokenExpiredError, InvalidRefreshTokenError, TokenTypeMismatchError, PasswordsNotMatchError
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


@pytest.mark.django_db
class TestVerifyTokenView:
    def setup_method(self):
        self.client = APIClient()
        self.data = {"token": "access_token"}

    @patch("store.service.authentication_service.VerifyTokenService.verify_token")
    def test_verify_token_success(self, mock_verify_token):
        mock_verify_token.return_value = {"msg": "Token is valid."}

        response = self.client.post("/verify_token/", self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["valid"] == True
        assert response.data["msg"] == "Token is valid."
        mock_verify_token.assert_called_once_with(self.data)

    @patch("store.service.authentication_service.VerifyTokenService.verify_token")
    def test_verify_token_expired(self, mock_verify_token):
        mock_verify_token.side_effect = jwt.ExpiredSignatureError("Token expired.")

        response = self.client.post("/verify_token/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["valid"] == False
        assert response.data["error"] == "Token expired."

    @patch("store.service.authentication_service.VerifyTokenService.verify_token")
    def test_verify_token_invalid(self, mock_verify_token):
        mock_verify_token.side_effect = jwt.InvalidTokenError("Invalid token.")

        response = self.client.post("/verify_token/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["valid"] == False
        assert response.data["error"] == "Invalid token."

    @patch("store.service.authentication_service.VerifyTokenService.verify_token")
    def test_verify_token_other_exception(self, mock_verify_token):
        mock_verify_token.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/verify_token/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_verify_account_serializer_error(self):
        response = self.client.post("/verify_token/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRefreshTokenView:
    def setup_method(self):
        self.client = APIClient()
        self.data = {"token": "refresh_token"}

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_success(self, mock_refresh_token):
        mock_refresh_token.return_value = "access_token"

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Access token successfully refreshed."
        assert response.data["access_token"] == "access_token"
        mock_refresh_token.assert_called_once_with(self.data)

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_expired(self, mock_refresh_token):
        mock_refresh_token.side_effect = RefreshTokenExpiredError("Refresh token expired.")

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["msg"] == "Failed to refresh access token."
        assert response.data["error"] == "Refresh token expired."

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_invalid(self, mock_refresh_token):
        mock_refresh_token.side_effect = InvalidRefreshTokenError("Invalid refresh token.")

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["msg"] == "Failed to refresh access token."
        assert response.data["error"] == "Invalid refresh token."

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_type_mismatch(self, mock_refresh_token):
        mock_refresh_token.side_effect = TokenTypeMismatchError("Access token instead of refresh token provided.")

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["msg"] == "Failed to refresh access token."
        assert response.data["error"] == "Access token instead of refresh token provided."

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_invalid_user_not_found(self, mock_refresh_token):
        mock_refresh_token.side_effect = UserNotFoundError("User not found.")

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "User not found."

    @patch("store.service.authentication_service.RefreshTokenService.refresh_access_token")
    def test_refresh_token_other_exception(self, mock_refresh_token):
        mock_refresh_token.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/refresh_token/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_refresh_account_serializer_error(self):
        response = self.client.post("/refresh_token/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestResetPassword:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.user_data["is_verified"] = True
        self.user = User.create_user(self.user_data)
        self.user.save()
        token = TokenGenerator.generate_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.data = {"password1": "ABC123abc#", "password2": "ABC123abc#", "code": "ABCabc123a"}

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_success(self, mock_reset_password):
        mock_reset_password.return_value = "Password changed successfully."

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Password changed successfully."
        mock_reset_password.assert_called_once_with(ANY, {"user": ANY, "code": "ABCabc123a", "password1": "ABC123abc#",
                "password2": "ABC123abc#",},)

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_verification_code_invalid(self, mock_reset_password):
        mock_reset_password.side_effect = InvalidVerificationCodeError("Refresh token expired.")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Verification code error."

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_verification_code_expired(self, mock_reset_password):
        mock_reset_password.side_effect = ExpiredVerificationCodeError("Verification code error.")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Verification code error."

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_passwords_not_match(self, mock_reset_password):
        mock_reset_password.side_effect = PasswordsNotMatchError("Changing password error.")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Changing password error."

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_token_invalid(self, mock_reset_password):
        mock_reset_password.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_reset_password_token_expired(self, mock_reset_password):
        mock_reset_password.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.ResetPasswordService.reset_password")
    def test_refresh_token_other_exception(self, mock_reset_password):
        mock_reset_password.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/reset_password/", self.data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_reset_password_serializer_error(self):
        response = self.client.post("/reset_password/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestResendVerificationCode:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.user_data["is_verified"] = True
        self.user = User.create_user(self.user_data)
        self.user.save()
        token = TokenGenerator.generate_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @patch("store.service.authentication_service.ResendVerificationCodeService.resend_verification_code")
    def test_resend_verification_code_success(self, mock_resend_verification_code):
        mock_resend_verification_code.return_value = "Verification code sent."

        response = self.client.post("/resend_verification_code/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Verification code sent."
        mock_resend_verification_code.assert_called_once_with(ANY, {"user": ANY})

    @patch("store.service.authentication_service.ResendVerificationCodeService.resend_verification_code")
    def test_resend_verification_code_token_expired(self, mock_resend_verification_code):
        mock_resend_verification_code.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/resend_verification_code/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.ResendVerificationCodeService.resend_verification_code")
    def test_resend_verification_code_cannot_get_token_from_request(self, mock_resend_verification_code):
        mock_resend_verification_code.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/resend_verification_code/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.authentication_service.ResendVerificationCodeService.resend_verification_code")
    def test_resend_verification_code_other_exception(self, mock_resend_verification_code):
        mock_resend_verification_code.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/resend_verification_code/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."
