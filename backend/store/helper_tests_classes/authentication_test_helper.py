from typing import Type
from unittest.mock import patch
import pytest
from store.models import User, UserPreferences, UserStatistics, Address, VerificationCode
from store.service.authentication_service import RegisterService


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