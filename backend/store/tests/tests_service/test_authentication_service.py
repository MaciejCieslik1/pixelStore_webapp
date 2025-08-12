import pytest
from unittest.mock import patch
from store.exceptions import UsernameAlreadyTakenError, EmailAlreadyTakenError
from store.helper_tests_classes.authentication_test_helper import RegistrationTestsHelper
from store.service.authentication_service import RegisterService
from store.models import User, UserPreferences, UserStatistics, Address, VerificationCode


@pytest.mark.django_db
class TestRegisterService:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = {"email": "test@example.com", "username": "tester", "password": "hashedpwd", "is_verified": False,
                "bio": "I'm new here!", "money": 0.00, "is_superuser": False, "last_login": None,
                "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

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
