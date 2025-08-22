import unittest

from store.models import User
from store.serializers.authentication_serializer import RegisterSerializer, LoginSerializer, \
    AccountVerificationSerializer, TokenVerificationSerializer, ResetPasswordSerializer, \
    ResendVerificationCodeSerializer


class TestRegisterSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"email": "test@example.com", "username": "tester", "password": "Abcdefg1#abc",
                "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.validated_data = {"email": "test@example.com", "username": "tester", "password": "Abcdefg1#abc",
                     "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

    def test_register_correct_data(self):
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_username_edge_case(self):
        self.data["username"] = "aaaaaaaaaaaaaaaa"
        self.validated_data["username"] = "aaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_min_username_edge_case(self):
        self.data["username"] = "aaa"
        self.validated_data["username"] = "aaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_min_password_edge_case(self):
        self.data["password"] = "testtR9#"
        self.validated_data["password"] = "testtR9#"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_password_edge_case(self):
        self.data["password"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["password"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_email_edge_case(self):
        self.data["email"] = "testtR9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com"
        self.validated_data["email"] = "testtR9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_address_edge_case(self):
        self.data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_city_edge_case(self):
        self.data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_data_max_country_edge_case(self):
        self.data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_correct_deleted_spaces(self):
        self.data = {"email": " test@example.com ", "username": " tester ", "password": " Abcdefg1#abc ",
                     "address": " fweffwe ", "postal_code": " 00001 ", "city": " Warsaw ", "country": " Poland "}
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_register_incorrect_no_username(self):
        self.data["username"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"username": "Username is not provided."})

    def test_register_incorrect_too_short_username(self):
        self.data["username"] = "aa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"username": "Username must be between 3 and 16 characters."})

    def test_register_incorrect_too_long_username(self):
        self.data["username"] = "aaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"username": "Username must be between 3 and 16 characters."})

    def test_register_incorrect_no_email(self):
        self.data["email"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not provided."})

    def test_register_incorrect_email_too_long(self):
        self.data["email"] = "testtR9aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email must have maximum 64 characters."})

    def test_register_incorrect_no_email_local_part(self):
        self.data["email"] = "@gmail.com"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not valid."})

    def test_register_incorrect_no_email_domain_part(self):
        self.data["email"] = "tester@.com"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not valid."})

    def test_register_incorrect_no_email_ending_part(self):
        self.data["email"] = "tester@gmail"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not valid."})

    def test_register_incorrect_no_password(self):
        self.data["password"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_register_incorrect_password_too_short(self):
        self.data["password"] = "testR9#"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password must be between 8 and 64 characters."})

    def test_register_incorrect_password_too_long(self):
        self.data["password"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password must be between 8 and 64 characters."})

    def test_register_incorrect_password_has_no_small_letter(self):
        self.data["password"] = "TESTTTT9#"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_register_incorrect_password_has_no_capital_letter(self):
        self.data["password"] = "testtt9#"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_register_incorrect_password_has_no_digits(self):
        self.data["password"] = "testRRR#"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_register_incorrect_password_has_no_special_character(self):
        self.data["password"] = "testRRR9"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_register_incorrect_no_address(self):
        self.data["address"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address is not provided."})

    def test_register_incorrect_too_long_address(self):
        self.data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address cannot be longer than 64 characters."})

    def test_register_incorrect_no_postal_code(self):
        self.data["postal_code"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code is not provided."})

    def test_register_incorrect_too_short_postal_code(self):
        self.data["postal_code"] = "0001"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code must have exactly 5 digits."})

    def test_register_incorrect_too_long_postal_code(self):
        self.data["postal_code"] = "000001"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code must have exactly 5 digits."})

    def test_register_incorrect_not_digit(self):
        self.data["postal_code"] = "00a01"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal must consist of exactly 5 digits."})

    def test_register_incorrect_no_city(self):
        self.data["city"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City is not provided."})

    def test_register_incorrect_too_long_city(self):
        self.data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City cannot be longer than 64 characters."})

    def test_register_incorrect_city_other_characters(self):
        self.data["city"] = "aaaaaa3fdf"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City should contain only letters."})

    def test_register_incorrect_no_country(self):
        self.data["country"] = ""
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country is not provided."})

    def test_register_incorrect_too_long_country(self):
        self.data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country cannot be longer than 64 characters."})

    def test_register_incorrect_country_other_characters(self):
        self.data["country"] = "aaaaaa3fdf"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country should contain only letters."})


class TestLoginSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"email": "test@example.com", "password": "Abcdefg1#abc"}
        self.validated_data = {"email": "test@example.com", "password": "Abcdefg1#abc"}

    def test_login_correct_data(self):
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_login_correct_data_delete_spaces(self):
        self.data = {"email": "     test@example.com     ", "password": "    Abcdefg1#abc   "}
        self.validated_data = {"email": "test@example.com", "password": "Abcdefg1#abc"}
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_login_incorrect_data_empty_email(self):
        self.data = {"email": "", "password": "Abcdefg1#abc"}
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not provided."})

    def test_login_incorrect_data_none_email(self):
        self.data = {"email": None, "password": "Abcdefg1#abc"}
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not provided."})

    def test_login_incorrect_data_empty_password(self):
        self.data = {"email": "test@example.com", "password": ""}
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_login_incorrect_data_none_password(self):
        self.data = {"email": "test@example.com", "password": None}
        serializer = LoginSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})


class TestVerifyAccountSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"email": "test@example.com", "verification_code": "ABCdef123a"}
        self.validated_data = {"email": "test@example.com", "verification_code": "ABCdef123a"}

    def test_verify_account_correct_data(self):
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_verify_account_correct_data_delete_spaces(self):
        self.data = {"email": "   test@example.com     ", "verification_code": "   ABCdef123a    "}
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_verify_account_incorrect_empty_email(self):
        self.data = {"email": "", "verification_code": "ABCdef123a"}
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not provided."})

    def test_verify_account_incorrect_none_email(self):
        self.data = {"email": None, "verification_code": "ABCdef123a"}
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"email": "Email is not provided."})

    def test_verify_account_incorrect_verification_code_too_short(self):
        self.data["verification_code"] = "ABC123abc"
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"verification_code": "Verification code must contain exactly 10 characters."})

    def test_verify_account_incorrect_verification_code_too_long(self):
        self.data["verification_code"] = "ABC123abc12"
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"verification_code": "Verification code must contain exactly 10 characters."})

    def test_verify_account_incorrect_empty_verification_code(self):
        self.data["verification_code"] = ""
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"verification_code": "Verification code is not provided."})

    def test_verify_account_incorrect_none_verification_code(self):
        self.data = {"email": "test@example.com", "verification_code": None}
        serializer = AccountVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"verification_code": "Verification code is not provided."})


class TestVerifyTokenSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTcwMDAwMDAwMH0.4B1D8eK6G7fG3Zx1y2A3hI5L6J7K8L9M0N1O2P3Q4R5"}
        self.validated_data = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTcwMDAwMDAwMH0.4B1D8eK6G7fG3Zx1y2A3hI5L6J7K8L9M0N1O2P3Q4R5"}

    def test_verify_token_correct_data(self):
        serializer = TokenVerificationSerializer(self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_verify_token_correct_data_delete_spaces(self):
        self.data = {"token": "    " + self.data["token"] + "   "}
        serializer = TokenVerificationSerializer(self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_verify_token_incorrect_empty_token(self):
        self.data = {"token": ""}
        serializer = TokenVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"token": "Token is not provided."})

    def test_verify_token_incorrect_none_token(self):
        self.data = {"token": None}
        serializer = TokenVerificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"token": "Token is not provided."})


class TestResetPasswordSerializer(unittest.TestCase):
    def setUp(self):
        user_creation_data = {"username": "tester", "email": "test@example.com", "password": "aaabb#123C"}
        self.user = User.create_user(user_creation_data)
        self.data = {"code": "ABC123abc2", "password1": "testeR9#", "password2": "testeR9#"}
        self.validated_data = {"user": self.user, "code": "ABC123abc2", "password1": "testeR9#", "password2": "testeR9#"}

    def test_reset_password_correct_data(self):
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_reset_password_correct_data_delete_spaces(self):
        self.data = {"code": "  ABC123abc2   ", "password1": "  testeR9#  ", "password2": "  testeR9#   "}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_reset_password_incorrect_none_user(self):
        serializer = ResetPasswordSerializer(data=self.data, user=None)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"user": "User is not provided."})

    def test_reset_password_incorrect_empty_code(self):
        self.data = {"code": "", "password1": "testeR9#", "password2": "testeR9#"}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"code": "Code is not provided."})

    def test_reset_password_incorrect_none_code(self):
        self.data = {"code": None, "password1": "testeR9#", "password2": "testeR9#"}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data,self.validated_data)
        self.assertEqual(serializer.errors, {"code": "Code is not provided."})

    def test_reset_password_incorrect_empty_password1(self):
        self.data = {"code": "ABC123abc2", "password1": "", "password2": "testeR9#"}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_reset_password_incorrect_none_password1(self):
        self.data = {"code": "ABC123abc2", "password1": None, "password2": "testeR9#"}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_reset_password_incorrect_empty_password2(self):
        self.data = {"code": "ABC123abc2", "password1": "testeR9#", "password2": ""}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_reset_password_incorrect_none_password2(self):
        self.data = {"code": "ABC123abc2", "password1": "testeR9#", "password2": None}
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password is not provided."})

    def test_reset_password_correct_data_min_passwords_edge_case(self):
        self.data["password1"] = "testtR9#"
        self.data["password2"] = "testtR9#"
        self.validated_data["password1"] = "testtR9#"
        self.validated_data["password2"] = "testtR9#"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_reset_password_correct_data_max_passwords_edge_case(self):
        self.data["password1"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.data["password2"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["password1"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["password2"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_reset_password_incorrect_password_has_no_capital_letter(self):
        self.data["password1"] = "testtt9#"
        self.data["password2"] = "testtt9#"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_reset_password_incorrect_password_has_no_digits(self):
        self.data["password1"] = "testRRR#"
        self.data["password2"] = "testRRR#"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_reset_password_incorrect_password_has_no_special_character(self):
        self.data["password1"] = "testRRR9"
        self.data["password2"] = "testRRR9"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password needs at least one small letter, \
                                                          capital letter, digit and special character."})

    def test_reset_password_incorrect_password_too_short(self):
        self.data["password1"] = "testR9#"
        self.data["password2"] = "testR9#"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password must be between 8 and 64 characters."})

    def test_reset_password_incorrect_password_too_long(self):
        self.data["password1"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.data["password2"] = "testtR9#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "Password must be between 8 and 64 characters."})

    def test_reset_password_incorrect_passwords_not_mach(self):
        self.data["password1"] = "testtR9#"
        self.data["password2"] = "testtR9#a"
        serializer = ResetPasswordSerializer(data=self.data, user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"password": "New passwords must match."})


class TestResendVerificationCodeSerializer(unittest.TestCase):
    def setUp(self):
        user_creation_data = {"username": "tester", "email": "test@example.com", "password": "aaabb#123C"}
        self.user = User.create_user(user_creation_data)
        self.validated_data = {"user": self.user}

    def test_resend_verification_code_correct_data(self):
        serializer = ResendVerificationCodeSerializer(user=self.user)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_resend_verification_code_incorrect_none_user(self):
        serializer = ResendVerificationCodeSerializer(user=None)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"user": "User is not provided."})
