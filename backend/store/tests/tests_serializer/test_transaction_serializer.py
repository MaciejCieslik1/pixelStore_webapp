import unittest
from decimal import Decimal

from store.serializers.transaction_serializer import CreateTransactionSerializer, UpdateTransactionSerializer


class TestCreateTransactionSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"buyer_username": "tester", "total_price": 10000}
        self.validated_data = {"buyer_username": "tester", "total_price": Decimal('10000')}

    def test_create_success(self):
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_create_success_string_big(self):
        self.data["total_price"] = "999999.99"
        self.validated_data["total_price"] = Decimal('999999.99')
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_create_success_string_small(self):
        self.data["total_price"] = "0.01"
        self.validated_data["total_price"] = Decimal('0.01')
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_create_success_string_other_separator(self):
        self.data["total_price"] = "0,01"
        self.validated_data["total_price"] = Decimal('0.01')
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_create_none_total_price(self):
        self.data["total_price"] = None
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price cannot be empty."})

    def test_create_total_price_too_small(self):
        self.data["total_price"] = 0
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price must be between 0.01 and 999999.99."})

    def test_create_product_rating_too_big(self):
        self.data["total_price"] = 1000000
        serializer = CreateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price must be between 0.01 and 999999.99."})


class TestUpdateTransactionSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"total_price": 10000, "is_finished": False}
        self.validated_data = {"total_price": Decimal('10000'), "is_finished": False}

    def test_update_success(self):
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_string_big(self):
        self.data["total_price"] = "999999.99"
        self.validated_data["total_price"] = Decimal('999999.99')
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_string_small(self):
        self.data["total_price"] = "0.01"
        self.validated_data["total_price"] = Decimal('0.01')
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_success_string_other_separator(self):
        self.data["total_price"] = "0,01"
        self.validated_data["total_price"] = Decimal('0.01')
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})


    def test_update_none_total_price(self):
        self.data["total_price"] = None
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price cannot be empty."})

    def test_update_total_price_too_small(self):
        self.data["total_price"] = 0
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price must be between 0.01 and 999999.99."})

    def test_update_product_rating_too_big(self):
        self.data["total_price"] = 1000000
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"total_price": "Total price must be between 0.01 and 999999.99."})

    def test_update_none_is_finished(self):
        self.data["is_finished"] = None
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"is_finished": "Is finished field cannot be empty."})

    def test_update_invalid_type_is_finished(self):
        self.data["is_finished"] = "yes"
        serializer = UpdateTransactionSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"is_finished": "Is finished field must be boolean."})
