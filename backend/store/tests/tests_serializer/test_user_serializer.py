import unittest
from decimal import Decimal

from store.serializers.user_serializer import UpdateUserSerializer


class TestUpdateUserSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"bio": "new bio", "money": "100.00"}
        self.validated_data = {"bio": "new bio", "money": Decimal('100.00')}

    def test_update_success(self):
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_money_big(self):
        self.data["money"] = "999999.99"
        self.validated_data["money"] = Decimal('999999.99')
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_money_small(self):
        self.data["money"] = "0.01"
        self.validated_data["money"] = Decimal('0.01')
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_money_other_separator(self):
        self.data["money"] = "0,01"
        self.validated_data["money"] = Decimal('0.01')
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_none_money(self):
        self.data["money"] = None
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"money": "Money cannot be empty."})

    def test_update_money_too_small(self):
        self.data["money"] = 0
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"money": "Money must be between 0.01 and 999999.99."})

    def test_update_product_money_too_big(self):
        self.data["money"] = 1000000
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"money": "Money must be between 0.01 and 999999.99."})

    def test_update_none_bio(self):
        self.data["bio"] = None
        self.validated_data["bio"] = ""
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_update_invalid_bio_type(self):
        self.data["bio"] = 12
        serializer = UpdateUserSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"bio": "Bio must be string."})
