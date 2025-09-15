import unittest

from store.serializers.order_product_serializer import (CreateOrderProductSerializer, UpdateOrderProductSerializer,
    FindByIdAndDeleteOrderProductSerializer)


class TestFindByIdOrderProductSerializer(unittest.TestCase):
    def test_find_by_id_success(self):
        order_product_id = 1
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.error, None)

    def test_find_by_id_empty_order_product_id(self):
        order_product_id = None
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id cannot be empty.")

    def test_find_by_id_string(self):
        order_product_id = "sfdfffs"
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")

    def test_find_by_id_not_positive_integer(self):
        order_product_id = 0
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")


class TestCreateOrderProductSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"product_id": 1, "transaction_id": 1, "seller_username": "tester", "shopping_price": 1000}
        self.validated_data = {"product_id": 1, "transaction_id": 1, "seller_username": "tester", "shopping_price": 1000}

    def test_create_success(self):
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_delete_spaces(self):
        self.data["seller_username"] = "  tester   "
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_shopping_price_max_integer(self):
        self.data["shopping_price"] = 999999
        self.validated_data["shopping_price"] = 999999
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_shopping_price_max_decimal(self):
        self.data["shopping_price"] = 999999.99
        self.validated_data["shopping_price"] = 999999.99
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_empty_product_id(self):
        self.data["product_id"] = None
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"product_id": "Product id cannot be empty."})

    def test_create_empty_transaction_id(self):
        self.data["transaction_id"] = None
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"transaction_id": "Transaction id cannot be empty."})

    def test_create_empty_seller_username(self):
        self.data["seller_username"] = None
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"seller_username": "Seller username cannot be empty."})

    def test_create_empty_shopping_price(self):
        self.data["shopping_price"] = None
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price cannot be empty."})

    def test_create_product_id_string(self):
        self.data["product_id"] = "sfdfffs"
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"product_id": "Product id must be positive integer."})

    def test_create_product_id_not_positive_integer(self):
        self.data["product_id"] = 0
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"product_id": "Product id must be positive integer."})

    def test_create_transaction_id_string(self):
        self.data["transaction_id"] = "sfdfffs"
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"transaction_id": "Transaction id must be positive integer."})

    def test_create_transaction_id_not_positive_integer(self):
        self.data["transaction_id"] = 0
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"transaction_id": "Transaction id must be positive integer."})

    def test_create_seller_username_int(self):
        self.data["seller_username"] = 1
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"seller_username": "Seller username must be string."})

    def test_create_shopping_price_string(self):
        self.data["shopping_price"] = "sfdfffs"
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be positive integer or decimal."})

    def test_create_shopping_price_not_positive_integer(self):
        self.data["shopping_price"] = 0
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be positive integer or decimal."})

    def test_create_shopping_price_too_big_integer(self):
        self.data["shopping_price"] = 1000000
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be less than 1000000.00."})

    def test_create_shopping_price_too_big_decimal(self):
        self.data["shopping_price"] = 1000000.00
        serializer = CreateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be less than 1000000.00."})


class TestUpdateOrderProductSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"shopping_price": 1000}

    def test_update_success(self):
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.errors, {})

    def test_update_shopping_price_max_integer(self):
        self.data["shopping_price"] = 999999
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.errors, {})

    def test_update_shopping_price_max_decimal(self):
        self.data["shopping_price"] = 999999.99
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.errors, {})

    def test_update_empty_shopping_price(self):
        self.data["shopping_price"] = None
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price cannot be empty."})

    def test_update_shopping_price_string(self):
        self.data["shopping_price"] = "sfdfffs"
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be positive integer or decimal."})

    def test_update_shopping_price_not_positive_integer(self):
        self.data["shopping_price"] = 0
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be positive integer or decimal."})

    def test_update_shopping_price_too_big_integer(self):
        self.data["shopping_price"] = 1000000
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be less than 1000000.00."})

    def test_update_shopping_price_too_big_decimal(self):
        self.data["shopping_price"] = 1000000.00
        serializer = UpdateOrderProductSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.errors, {"shopping_price": "Shopping price must be less than 1000000.00."})


class TestDeleteOrderProductSerializer(unittest.TestCase):
    def test_delete_success(self):
        order_product_id = 1
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.error, None)

    def test_delete_empty_order_product_id(self):
        order_product_id = None
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id cannot be empty.")

    def test_delete_string(self):
        order_product_id = "sfdfffs"
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")

    def test_delete_not_positive_integer(self):
        order_product_id = 0
        serializer = FindByIdAndDeleteOrderProductSerializer(order_product_id=order_product_id)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertEqual(serializer.error, "Order product id must be positive integer.")
