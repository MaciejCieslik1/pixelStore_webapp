import unittest
from store.models import User, Transaction, Product, OrderProduct, OrderReturn
from datetime import datetime


class TestOrderReturnModel(unittest.TestCase):
    def setUp(self):
        self.seller = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                           bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.transaction = Transaction(buyer=self.seller, total_price=0, date_time=datetime.now(), is_finished=False)
        self.product = Product(owner=self.seller, name="cpu", description="dsfffefee", price=1000, amount=2,
                               color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                               status=Product.ProductStatus.AVAILABLE)
        self.order_product = OrderProduct(transaction=self.transaction, product=self.product,
                                      seller=self.seller, shopping_price=20)

    def test_eq_same_data(self):
        order_return1 = OrderReturn(order_product=self.order_product, description="return",
                                      return_date_time=datetime.now(), is_accepted=True)
        order_return2 = OrderReturn(order_product=self.order_product, description="return",
                                      return_date_time=datetime.now(), is_accepted=True)

        self.assertEqual(order_return1, order_return2)

    def test_eq_different_data(self):
        order_return1 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=True)
        order_return2 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=False)

        self.assertNotEquals(order_return1, order_return2)

    def test_hash_same_data(self):
        order_return1 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=True)
        order_return2 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=True)

        self.assertEqual(hash(order_return1), hash(order_return2))

    def test_hash_different_data(self):
        order_return1 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=True)
        order_return2 = OrderReturn(order_product=self.order_product, description="return",
                                    return_date_time=datetime.now(), is_accepted=False)

        self.assertNotEquals(hash(order_return1), hash(order_return2))

if __name__ == "__main__":
    unittest.main()
