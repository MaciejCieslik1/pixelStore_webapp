from datetime import datetime
from typing import Type
from unittest.mock import patch
from rest_framework.test import APIClient

import jwt
import pytest

from config import settings_test
from store.helper_classes.authentication_helper import TokenGenerator
from store.models import User, UserPreferences, UserStatistics, Address, VerificationCode
from store.service.authentication_service import RegisterService, LoginService, ResetPasswordService, \
    VerifyAccountService, ResendVerificationCodeService


class RegistrationTestsHelper:
    @staticmethod
    def handle_double_registration_process(user_data: dict, new_user_data: dict, exception: Type[BaseException],
                                           message: str) -> dict:
        rows_count = {}
        rows_count["users_before"], rows_count["user_prefs_before"], rows_count["user_stats_before"], \
            rows_count["addresses_before"], rows_count["verif_codes_before"] = RegistrationTestsHelper.count_rows()

        service = RegisterService()
        with patch("store.service.authentication_service.EmailSender.send_code") as mock_send:
            service.register_user(user_data)
        with pytest.raises(exception) as e:
            service.register_user(new_user_data)
        assert f"User with this {message} already exists." in str(e.value)
        mock_send.assert_called_once()

        rows_count["users_after"], rows_count["user_prefs_after"], rows_count["user_stats_after"], \
            rows_count["addresses_after"], rows_count["verif_codes_after"] = RegistrationTestsHelper.count_rows()

        return rows_count

    @staticmethod
    def count_rows() -> tuple[int, int, int, int, int]:
        return (User.objects.count(), UserPreferences.objects.count(), UserStatistics.objects.count(),
                Address.objects.count(), VerificationCode.objects.count())

    @staticmethod
    def assert_rows_count(rows_count: dict, additional_rows_number: int):
        assert rows_count["users_after"]  == rows_count["users_before"] + additional_rows_number
        assert rows_count["user_prefs_after"] == rows_count["user_prefs_before"] + additional_rows_number
        assert rows_count["user_stats_after"] == rows_count["user_stats_before"] + additional_rows_number
        assert rows_count["addresses_after"] == rows_count["addresses_before"] + additional_rows_number
        assert rows_count["verif_codes_after"] == rows_count["verif_codes_before"] + additional_rows_number


class LoginTestsHelper:
    @staticmethod
    def handle_login_process(user_data: dict, exception: Type[BaseException], message: str):
        user = User.objects.get(username="tester")
        token_version_before = user.token_version
        login_service = LoginService()

        with pytest.raises(exception) as e:
            login_service.login_user(user_data)

        assert f"{message}" in str(e.value)
        user = User.objects.get(username="tester")
        token_version_after = user.token_version

        assert token_version_after == token_version_before

SECRET_KEY = settings_test.SECRET_KEY
ALGORITHM = 'HS256'

class TokenTestsHelper:
    @staticmethod
    def generate_refresh_token(user_id: int, token_type: str, exp: datetime, iat: datetime):
        return jwt.encode({
            "user_id": user_id,
            "token_type": token_type,
            "jti": "test",
            "exp": exp,
            "iat": iat,
        }, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def generate_access_token(user_id: int, token_type: str, exp: datetime, iat: datetime, token_version: int):
        return jwt.encode({
            "user_id": user_id,
            "token_type": token_type,
            "jti": "test",
            "exp": exp,
            "iat": iat,
            "token_version": token_version,
        }, SECRET_KEY, algorithm=ALGORITHM)


class AuthenticationHelper:
    @staticmethod
    def register_and_verify_user(user_data: dict):
        AuthenticationHelper.register_user(user_data)
        verify_account_service = VerifyAccountService()
        user = User.objects.get(username=user_data["username"])
        user_data["code"] = user.verification_code.code
        verify_account_service.verify_account(user_data)

    @staticmethod
    def register_user(user_data: dict):
        register_service = RegisterService()
        register_service.register_user(user_data)

    @staticmethod
    def login_user(user_data: dict) -> str:
        login_service = LoginService()
        result = login_service.login_user(user_data)
        return result["access_token"]

    @staticmethod
    def login_user_return_refresh_token(user_data: dict) -> str:
        login_service = LoginService()
        result = login_service.login_user(user_data)
        return result["refresh_token"]

    @staticmethod
    def register_and_login_user(user_data: dict) -> str:
        AuthenticationHelper.register_and_verify_user(user_data)
        return AuthenticationHelper.login_user(user_data)

    @staticmethod
    def return_exemplary_user_data() -> dict:
        return {"email": "test@example.com", "username": "tester", "password": "Abc123#ab",
         "is_verified": False, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
         "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}


class ResetPasswordTestsHelper:
    @staticmethod
    def handle_access_token_error(access_token: str, exception: Type[BaseException], message: str):
        reset_password_service = ResetPasswordService()
        user = User.objects.get(username="tester")
        data = {"user": user, "code": user.verification_code, "password1": "fdfddfffd", "password2": "fdfddfffd"}

        with pytest.raises(exception) as e:
            reset_password_service.reset_password(access_token, data)
        assert f"{message}" in str(e.value)


class ResendVerificationCodeTestsHelper:
    @staticmethod
    def handle_resend_verification_code_error(verification_code_before: str, access_token: str, data: dict,
                                              exception: Type[BaseException], message: str):
        resend_verification_code_service = ResendVerificationCodeService()
        with pytest.raises(exception) as e:
            resend_verification_code_service.resend_verification_code(access_token, data)
        user = User.objects.get(username="tester")
        verification_code_after = user.verification_code.code

        assert f"{message}" in str(e.value)
        assert verification_code_before == verification_code_after


def create_api_client_with_user():
    client = APIClient()
    user_data = AuthenticationHelper.return_exemplary_user_data()
    user_data["is_verified"] = True
    user = User.create_user(user_data)
    user.save()
    token = TokenGenerator.generate_access_token(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client, user