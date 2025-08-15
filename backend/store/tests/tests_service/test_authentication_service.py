from datetime import timedelta
from django.utils import timezone
import jwt
import pytest
from unittest.mock import patch
from config import settings_test
from store.exceptions import UsernameAlreadyTakenError, EmailAlreadyTakenError, UserNotVerifiedError, \
    InvalidVerificationCodeError, UserNotFoundError, InvalidPasswordError, ExpiredVerificationCodeError, \
    TokenExpiredError, IncorrectTokenError, TokenExpiredByReplacementError, RefreshTokenExpiredError, \
    InvalidRefreshTokenError, TokenTypeMismatchError, PasswordsNotMatchError
from store.helper_tests_classes.authentication_test_helper import RegistrationTestsHelper, LoginTestsHelper, \
    AuthenticationHelper, TokenTestsHelper, ResetPasswordTestsHelper, ResendVerificationCodeTestsHelper
from store.service.authentication_service import RegisterService, LoginService, VerifyAccountService, LogoutService, \
    VerifyTokenService, RefreshTokenService, ResetPasswordService, ResendVerificationCodeService
from store.models import User, UserPreferences, UserStatistics, Address, VerificationCode


@pytest.mark.django_db
class TestRegisterService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = self.user_data = AuthenticationHelper.return_exemplary_user_data()

    def test_register_user_saves_to_db(self):
        rows_count = {}
        rows_count["users_before"], rows_count["user_prefs_before"], rows_count["user_stats_before"], \
            rows_count["addresses_before"], rows_count["verif_codes_before"] = RegistrationTestsHelper.count_rows()

        with patch("store.service.authentication_service.EmailSender.send_code") as mock_send:
            service = RegisterService()
            result = service.register_user(self.user_data)

        rows_count["users_after"], rows_count["user_prefs_after"], rows_count["user_stats_after"], \
            rows_count["addresses_after"], rows_count["verif_codes_after"] = RegistrationTestsHelper.count_rows()

        user = User.objects.get(username="tester")
        mock_send.assert_called_once()
        email_arg, code_arg = mock_send.call_args[0]

        assert result == "User tester registered successfully"
        additional_rows_number = 1
        RegistrationTestsHelper.assert_rows_count(rows_count, additional_rows_number)
        assert User.objects.filter(email="test@example.com", username="tester").exists()
        assert UserPreferences.objects.filter(user=user).exists()
        assert UserStatistics.objects.filter(user=user).exists()
        assert Address.objects.filter(user=user).exists()
        assert VerificationCode.objects.filter(user=user).exists()
        assert email_arg == "test@example.com"

    def test_register_user_raises_email_exception(self):
        new_data = {"email": "test@example.com", "username": "tester1", "password": "hashedpwd", "is_verified": False,
                     "bio": "I'm new here!", "money": 0.00, "is_superuser": False, "last_login": None,
                     "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

        rows_count = RegistrationTestsHelper.handle_double_registration_process(self.user_data, new_data,
                                                                            EmailAlreadyTakenError, "email")

        additional_rows_number = 1
        RegistrationTestsHelper.assert_rows_count(rows_count, additional_rows_number)

    def test_register_user_raises_username_exception(self):
        new_data = {"email": "test1@example.com", "username": "tester", "password": "hashedpwd", "is_verified": False,
                    "bio": "I'm new here!", "money": 0.00, "is_superuser": False, "last_login": None,
                    "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

        rows_count = RegistrationTestsHelper.handle_double_registration_process(self.user_data,
                    new_data, UsernameAlreadyTakenError,"username")

        additional_rows_number = 1
        RegistrationTestsHelper.assert_rows_count(rows_count, additional_rows_number)

@pytest.mark.django_db
class TestLoginService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        AuthenticationHelper.register_and_verify_user(self.user_data)

    def test_login_user_successfully(self):
        user = User.objects.get(username="tester")
        token_version_before = user.token_version
        login_service = LoginService()

        with patch("store.helper_classes.authentication_helper.TokenGenerator.generate_access_token",
                   return_value="access123") as mock_access, \
            patch("store.helper_classes.authentication_helper.TokenGenerator.generate_refresh_token",
                  return_value="refresh123") as mock_refresh:
            result = login_service.login_user(self.user_data)
        user = User.objects.get(username="tester")
        token_version_after = user.token_version

        assert result["access_token"] == "access123"
        assert result["refresh_token"] == "refresh123"
        mock_access.assert_called_once()
        mock_refresh.assert_called_once()
        assert token_version_after == token_version_before + 1

    def test_login_user_not_verified(self):
        user = User.objects.get(username="tester")
        user.is_verified = False
        user.save()

        LoginTestsHelper.handle_login_process(self.user_data, UserNotVerifiedError, "User not verified.")

    def test_login_user_invalid_email(self):
        self.user_data["email"] = "test1@example.com"
        login_service = LoginService()

        with pytest.raises(UserNotFoundError) as e:
            login_service.login_user(self.user_data)

        assert f"User with provided email not found." in str(e.value)

    def test_login_user_invalid_password(self):
        self.user_data["password"] = "invalid_password"

        LoginTestsHelper.handle_login_process(self.user_data, InvalidPasswordError, "Invalid password.")


@pytest.mark.django_db
class TestLogoutService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.access_token = AuthenticationHelper.register_and_login_user(self.user_data)

    def test_logout_successfully(self):
        logout_service = LogoutService()
        user = User.objects.get(username="tester")

        result = logout_service.logout_user(self.access_token, user)

        assert result == "User successfully logged out."

    def test_logout_expired_access_token(self):
        user = User.objects.get(username="tester")
        access_token = TokenTestsHelper.generate_access_token(user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        logout_service = LogoutService()
        user = User.objects.get(username="tester")

        with pytest.raises(TokenExpiredError) as e:
            logout_service.logout_user(access_token, user)
        assert f"Access token has expired." in str(e.value)

    def test_logout_incorrect_access_token(self):
        access_token = "invalid token"
        logout_service = LogoutService()
        user = User.objects.get(username="tester")

        with pytest.raises(IncorrectTokenError) as e:
            logout_service.logout_user(access_token, user)
        assert f"Incorrect access token." in str(e.value)

    def test_logout_expired_by_replacement_access_token(self):
        access_token_first = self.access_token
        logout_service = LogoutService()
        user = User.objects.get(username="tester")
        logout_service.logout_user(access_token_first, user)
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")

        with pytest.raises(TokenExpiredByReplacementError) as e:
            logout_service.logout_user(access_token_first, user)
        assert f"Access token is no longer valid." in str(e.value)


@pytest.mark.django_db
class TestVerifyAccountService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        register_service = RegisterService()
        register_service.register_user(self.user_data)

    def test_verify_account_successfully(self):
        verify_account_service = VerifyAccountService()
        user = User.objects.get(username="tester")
        self.user_data["code"] = user.verification_code.code

        with patch("store.service.authentication_service.EmailSender.send_code") as mock_send:
            verify_account_service.verify_account(self.user_data)

        user = User.objects.get(username="tester")
        is_verified_after = user.is_verified
        email, code = mock_send.call_args[0]

        mock_send.assert_called_once()
        assert is_verified_after == True
        assert user.verification_code.code != self.user_data["code"]
        assert email == "test@example.com"

    def test_verify_account_invalid_code(self):
        verify_account_service = VerifyAccountService()
        self.user_data["code"] = "bad_code"
        user = User.objects.get(username="tester")
        code_before = user.verification_code.code

        with patch("store.service.authentication_service.EmailSender.send_code"):
            with pytest.raises(InvalidVerificationCodeError) as e:
                verify_account_service.verify_account(self.user_data)

        user = User.objects.get(username="tester")
        is_verified_after = user.is_verified
        code_after = user.verification_code.code

        assert f"Incorrect verification code." in str(e.value)
        assert is_verified_after == False
        assert code_before == code_after


    def test_verify_account_code_expired(self):
        verify_account_service = VerifyAccountService()
        user = User.objects.get(username="tester")
        code_before = user.verification_code.code
        user.verification_code.expiration_date_time = timezone.now() - timedelta(days=1)
        user.verification_code.save()
        self.user_data["code"] = code_before

        with pytest.raises(ExpiredVerificationCodeError) as e:
            verify_account_service.verify_account(self.user_data)
        assert f"Verification code has expired." in str(e.value)

        user = User.objects.get(username="tester")
        is_verified_after = user.is_verified

        assert is_verified_after == False

    def test_verify_account_user_invalid_email(self):
        self.user_data["email"] = "test1@example.com"
        verify_account_service = VerifyAccountService()

        with pytest.raises(UserNotFoundError) as e:
            verify_account_service.verify_account(self.user_data)

        assert f"User with provided email does not exist." in str(e.value)

SECRET_KEY = settings_test.SECRET_KEY
ALGORITHM = 'HS256'

@pytest.mark.django_db
class TestVerifyTokenService:
    def test_verify_token_valid(self):
        service = VerifyTokenService()
        data = {"token": "fake_token"}

        with patch("jwt.decode") as mock_decode:
            service.verify_token(data)
        mock_decode.assert_called_once_with("fake_token", SECRET_KEY, algorithms=[ALGORITHM])

    def test_verify_token_invalid(self):
        service = VerifyTokenService()
        data = {"token": "bad_token"}

        with patch("jwt.decode", side_effect=jwt.exceptions.InvalidTokenError):
            with pytest.raises(jwt.exceptions.InvalidTokenError):
                service.verify_token(data)


@pytest.mark.django_db
class TestRefreshTokenService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        AuthenticationHelper.register_and_verify_user(self.user_data)

    def test_refresh_access_token_successfully(self):
        data = {"refresh_token": AuthenticationHelper.login_user_return_refresh_token(self.user_data)}
        user = User.objects.get(username="tester")
        service = RefreshTokenService()

        access_token = service.refresh_access_token(data)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        assert user.user_id == payload.get("user_id")
        assert "access" == payload.get("token_type")
        assert user.token_version == payload.get("token_version")

    def test_refresh_access_token_invalid_user_id(self):
        data = {"refresh_token": AuthenticationHelper.login_user_return_refresh_token(self.user_data)}
        service = RefreshTokenService()

        with patch("store.service.authentication_service.RefreshTokenService._get_user_id_from_refresh_token",
                   return_value="123"):
            with pytest.raises(UserNotFoundError) as e:
                service.refresh_access_token(data)

        assert f"User with provided id not found." in str(e.value)

    def test_refresh_access_token_expired(self):
        user = User.objects.get(username="tester")
        data = {"refresh_token": TokenTestsHelper.generate_refresh_token(user.user_id,
                "refresh", timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2))}
        service = RefreshTokenService()

        with pytest.raises(RefreshTokenExpiredError) as e:
            service.refresh_access_token(data)

        assert f"Refresh token has expired." in str(e.value)

    def test_refresh_access_token_invalid(self):
        data = {"refresh_token": "bad_token"}
        service = RefreshTokenService()

        with pytest.raises(InvalidRefreshTokenError) as e:
            service.refresh_access_token(data)

        assert f"Refresh token is invalid." in str(e.value)

    def test_refresh_access_token_wrong_type(self):
        user = User.objects.get(username="tester")
        data = {"refresh_token": TokenTestsHelper.generate_refresh_token(user.user_id + 10,
                "access", timezone.now() + timedelta(days=1), timezone.now() - timedelta(days=2))}
        service = RefreshTokenService()

        with pytest.raises(TokenTypeMismatchError) as e:
            service.refresh_access_token(data)

        assert f"Provided token is not a refresh token." in str(e.value)


@pytest.mark.django_db
class TestResetPasswordService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.access_token = AuthenticationHelper.register_and_login_user(self.user_data)

    def test_reset_password_successfully(self):
        reset_password_service = ResetPasswordService()
        user = User.objects.get(username="tester")
        data = {"user": user, "code": user.verification_code.code, "password1": "aaaaa", "password2": "aaaaa"}

        reset_password_service.reset_password(self.access_token, data)

    def test_reset_password_expired_access_token(self):
        user = User.objects.get(username="tester")
        access_token = TokenTestsHelper.generate_access_token(user.user_id, "access",
                                                              timezone.now() - timedelta(days=1),
                                                              timezone.now() - timedelta(days=2),
                                                              token_version=1)
        ResetPasswordTestsHelper.handle_access_token_error(access_token, TokenExpiredError,
                                                           "Access token has expired.")

    def test_reset_password_incorrect_access_token(self):
        access_token = "invalid token"
        ResetPasswordTestsHelper.handle_access_token_error(access_token, IncorrectTokenError,
                                                           "Incorrect access token.")

    def test_reset_password_expired_by_replacement_access_token(self):
        reset_password_service = ResetPasswordService()
        login_service = LoginService()
        login_service.login_user(self.user_data)
        user = User.objects.get(username="tester")
        data = {"user": user, "code": user.verification_code.code, "password1": "fdfddfffd", "password2": "fdfddfffd"}

        with pytest.raises(TokenExpiredByReplacementError) as e:
            reset_password_service.reset_password(self.access_token, data)
        assert f"Access token is no longer valid." in str(e.value)

    def test_reset_password_invalid_verification_code(self):
        reset_password_service = ResetPasswordService()
        user = User.objects.get(username="tester")
        data = {"user": user, "code": "bad_code", "password1": "fdfddfffd", "password2": "fdfddfffd"}

        with pytest.raises(InvalidVerificationCodeError) as e:
            reset_password_service.reset_password(self.access_token, data)
        assert f"Incorrect verification code." in str(e.value)

    def test_reset_password_passwords_dont_match(self):
        reset_password_service = ResetPasswordService()
        user = User.objects.get(username="tester")
        data = {"user": user, "code": user.verification_code.code, "password1": "aaaaa", "password2": "bbbbbb"}

        with pytest.raises(PasswordsNotMatchError) as e:
            reset_password_service.reset_password(self.access_token, data)
        assert f"Passwords don't match." in str(e.value)


@pytest.mark.django_db
class TestResendVerificationCodeService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.access_token = AuthenticationHelper.register_and_login_user(self.user_data)

    def test_resend_verification_code_successfully(self):
        user = User.objects.get(username="tester")
        data = {"user": user}
        verification_code_before = user.verification_code
        resend_verification_code_service = ResendVerificationCodeService()

        with patch("store.service.authentication_service.EmailSender.send_code") as mock_send:
            resend_verification_code_service.resend_verification_code(self.access_token, data)
            mock_send.assert_called_once()

        user = User.objects.get(username="tester")
        verification_code_after = user.verification_code

        assert verification_code_before != verification_code_after

    def test_resend_verification_code_expired_access_token(self):
        user = User.objects.get(username="tester")
        access_token = TokenTestsHelper.generate_access_token(user.user_id, "access",
                                                                            timezone.now() - timedelta(days=1),
                                                                            timezone.now() - timedelta(days=2),
                                                                            token_version=1)
        verification_code_before = user.verification_code
        resend_verification_code_service = ResendVerificationCodeService()
        user = User.objects.get(username="tester")
        data = {"user": user}

        with pytest.raises(TokenExpiredError) as e:
            resend_verification_code_service.resend_verification_code(access_token, data)
        user = User.objects.get(username="tester")
        verification_code_after = user.verification_code

        assert f"Access token has expired." in str(e.value)
        assert verification_code_before == verification_code_after

    def test_resend_verification_code_incorrect_access_token(self):
        access_token = "invalid token"
        user = User.objects.get(username="tester")
        verification_code_before = user.verification_code.code
        data = {"user": user}

        ResendVerificationCodeTestsHelper.handle_resend_verification_code_error(verification_code_before,
            access_token, data, IncorrectTokenError,"Incorrect access token.")

    def test_resend_verification_code_expired_by_replacement_access_token(self):
        access_token_first = self.access_token
        logout_service = LogoutService()
        user = User.objects.get(username="tester")
        logout_service.logout_user(access_token_first, user)
        old_token_version = user.token_version
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        verification_code_before = user.verification_code.code
        data = {"user": user}

        ResendVerificationCodeTestsHelper.handle_resend_verification_code_error(verification_code_before,
            access_token_first, data, TokenExpiredByReplacementError, "Access token is no longer valid.")

        user = User.objects.get(username="tester")
        assert old_token_version != user.token_version
