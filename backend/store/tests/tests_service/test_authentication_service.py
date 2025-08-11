import pytest
from unittest.mock import patch
from store.service.authentication_service import RegisterService
from store.models import User, UserPreferences, UserStatistics, Address, VerificationCode

@pytest.mark.django_db
def test_register_user_saves_to_db():
    data = {"email": "sender@example.com", "username": "testuser1", "password": "hashedpwd", "is_verified": False,
            "bio": "I'm new here!", "money": 0.00, "is_superuser": False, "last_login": None,
            "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

    users_before = User.objects.count()
    user_preferences_before = UserPreferences.objects.count()
    user_statistics_before = UserStatistics.objects.count()
    addresses_before = Address.objects.count()
    verification_codes_before = VerificationCode.objects.count()
    with patch("store.service.authentication_service.EmailSender.send_code") as mock_send:
        service = RegisterService()
        result = service.register_user(data)

    users_after = User.objects.count()
    user_preferences_after = UserPreferences.objects.count()
    user_statistics_after = UserStatistics.objects.count()
    addresses_after = Address.objects.count()
    verification_codes_after = VerificationCode.objects.count()

    user = User.objects.get(username="tester")
    mock_send.assert_called_once()
    email_arg, code_arg = mock_send.call_args[0]

    assert result == "User tester registered successfully"
    assert users_after == users_before + 1
    assert user_preferences_after == user_preferences_before + 1
    assert user_statistics_after == user_statistics_before + 1
    assert addresses_after == addresses_before + 1
    assert verification_codes_after == verification_codes_before + 1
    assert User.objects.filter(email="test@example.com", username="tester").exists()
    assert UserPreferences.objects.filter(user=user).exists()
    assert UserStatistics.objects.filter(user=user).exists()
    assert Address.objects.filter(user=user).exists()
    assert VerificationCode.objects.filter(user=user).exists()
    assert email_arg == "test@example.com"
