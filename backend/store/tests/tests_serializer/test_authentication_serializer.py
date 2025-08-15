import unittest

from store.serializers.authentication_serializer import RegisterSerializer


class TestRegisterSerializer(unittest.TestCase):
    pass
    # def test_register_correct_data(self):
    #     data = {"email": "test@example.com", "username": "tester", "password": "Abcdefg1#abc", "is_verified": False,
    #             "bio": "I'm new here!", "money": 0.00, "is_superuser": False, "last_login": None,
    #             "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
    #
    #     serializer = RegisterSerializer(data=data)
    #
    #     self.assertEqual(serializer.is_valid(), True)
    #     self.assertEqual(serializer.validated_data, data)
    #     self.assertEqual(serializer.errors, {})
