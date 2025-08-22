import unittest

from store.serializers.address_serializer import UpdateAddressSerializer


class TestUpdateAddressSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"address": "example_street", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        self.validated_data = {"address": "example_street", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}

    def test_update_address_success(self):
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_address_success_delete_spaces(self):
        self.data = {"address": "  example_street  ", "postal_code": "  00001  ", "city": "  Warsaw ", "country": "  Poland  "}
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_address_correct_data_max_address_edge_case(self):
        self.data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_address_correct_data_max_city_edge_case(self):
        self.data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_address_correct_data_max_country_edge_case(self):
        self.data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self.validated_data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, True)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_address_empty_address(self):
        self.data["address"] = ""
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address is not provided."})

    def test_update_address_none_address(self):
        self.data["address"] = None
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address is not provided."})

    def test_update_postal_code_empty_postal_code(self):
        self.data["postal_code"] = ""
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code is not provided."})

    def test_update_postal_code_none_postal_code(self):
        self.data["postal_code"] = None
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code is not provided."})

    def test_update_city_empty_city(self):
        self.data["city"] = ""
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City is not provided."})

    def test_update_city_none_city(self):
        self.data["city"] = None
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City is not provided."})

    def test_update_country_empty_country(self):
        self.data["country"] = ""
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country is not provided."})

    def test_update_country_none_country(self):
        self.data["country"] = None
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country is not provided."})

    def test_update_postal_code_invalid_lenght(self):
        self.data["postal_code"] = "000001"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal code must have exactly 5 digits."})

    def test_update_postal_code_invalid_chars(self):
        self.data["postal_code"] = "0001w"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"postal_code": "Postal must consist of exactly 5 digits."})

    def test_update_city_invalid_digits(self):
        self.data["city"] = "Warsaw1"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City should contain only letters."})

    def test_update_country_invalid_digits(self):
        self.data["country"] = "Poland1"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country should contain only letters."})

    def test_update_address_incorrect_too_long_address(self):
        self.data["address"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"address": "Address cannot be longer than 64 characters."})

    def test_update_address_incorrect_too_long_city(self):
        self.data["city"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"city": "City cannot be longer than 64 characters."})

    def test_update_address_incorrect_too_long_country(self):
        self.data["country"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        serializer = UpdateAddressSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertEqual(result, False)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"country": "Country cannot be longer than 64 characters."})
