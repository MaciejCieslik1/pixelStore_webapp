import unittest
from store.models import User, Transaction, Product, OrderProduct
from datetime import datetime


class TestOrderProductModel(unittest.TestCase):
    def setUp(self):
        self.seller = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                           bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.transaction = Transaction(buyer=self.seller, total_price=0, date_time=datetime.now(), is_finished=False)
        self.product = Product(owner=self.seller, name="cpu", description="dsfffefee", price=1000, amount=2,
            color="red", weight=3, length= 2, width=0.5, height=1.1, guarantee_period=4,
            status=Product.ProductStatus.AVAILABLE)

    def test_eq_same_data(self):
        order_product1 = OrderProduct(transaction=self.transaction, product=self.product,
            seller=self.seller, shopping_price=20)
        order_product2 = OrderProduct(transaction=self.transaction, product=self.product,
                                     seller=self.seller, shopping_price=20)

        self.assertEqual(order_product1, order_product2)

    def test_eq_different_data(self):
        order_product1 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=20)
        order_product2 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=10)

        self.assertNotEqual(order_product1, order_product2)

    def test_hash_same_data(self):
        order_product1 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=20)
        order_product2 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=20)

        self.assertEqual(hash(order_product1), hash(order_product2))

    def test_hash_different_data(self):
        order_product1 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=20)
        order_product2 = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=10)

        self.assertNotEqual(hash(order_product1), hash(order_product2))

if __name__ == "__main__":
    unittest.main()
