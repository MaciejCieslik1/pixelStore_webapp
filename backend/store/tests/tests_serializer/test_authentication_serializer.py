import unittest

from store.serializers.authentication_serializer import RegisterSerializer, LoginSerializer


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

    def test_register_incorrect_address_other_characters(self):
        self.data["address"] = "aaaaaa3fdf"
        serializer = RegisterSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address should contain only letters."})

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
        self.data = {"email": "", "password": "Abcdefg1#abc"}
        self.validated_data = {"email": None, "password": "Abcdefg1#abc"}
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


