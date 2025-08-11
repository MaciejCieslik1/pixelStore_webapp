import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from store.models import User, VerificationCode


class TestVerificationCodeModel(unittest.TestCase):
    def setUp(self):
        self.user = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                     bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.now = datetime.now()

    def test_eq_same_data(self):
        verification_code1 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                           expiration_date_time=self.now)
        verification_code2 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                              expiration_date_time=self.now)

        self.assertEqual(verification_code1, verification_code2)

    def test_eq_different_data(self):
        verification_code1 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                              expiration_date_time=self.now)
        verification_code2 = VerificationCode(user=self.user, code="0123456789", creation_date_time=self.now,
                                              expiration_date_time=self.now)

        self.assertNotEqual(verification_code1, verification_code2)

    def test_hash_same_data(self):
        verification_code1 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                              expiration_date_time=self.now)
        verification_code2 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                              expiration_date_time=self.now)

        self.assertEqual(hash(verification_code1), hash(verification_code2))

    def test_hash_different_data(self):
        verification_code1 = VerificationCode(user=self.user, code="1234567890", creation_date_time=self.now,
                                              expiration_date_time=self.now)
        verification_code2 = VerificationCode(user=self.user, code="0123456789", creation_date_time=self.now,
                                              expiration_date_time=self.now)

        self.assertNotEqual(hash(verification_code1), hash(verification_code2))

    @patch('store.models.verification_code.random.choices', return_value=list("ABC123XYZ0"))
    @patch('store.models.verification_code.timezone.now')
    def test_create_verification_code(self, mock_now, mock_choices):
        fixed_time = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
        mock_now.return_value = fixed_time

        verification_code = VerificationCode.create_verification_code(self.user)

        self.assertEqual(verification_code.user, self.user)
        self.assertEqual(verification_code.code, "ABC123XYZ0")
        self.assertEqual(verification_code.creation_date_time, fixed_time)
        self.assertEqual(verification_code.expiration_date_time, fixed_time + timedelta(minutes=15))
