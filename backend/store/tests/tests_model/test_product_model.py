import unittest
from store.models import User, Product


class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.owner = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                           bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)

    def test_eq_same_data(self):
        product1 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                               color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                               status=Product.ProductStatus.AVAILABLE)
        product2 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                               color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                               status=Product.ProductStatus.AVAILABLE)

        self.assertEqual(product1, product2)

    def test_eq_different_data(self):
        product1 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)
        product2 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.UNAVAILABLE)

        self.assertNotEqual(product1, product2)

    def test_hash_same_data(self):
        product1 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)
        product2 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)

        self.assertEqual(hash(product1), hash(product2))

    def test_hash_different_data(self):
        product1 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)
        product2 = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.UNAVAILABLE)

        self.assertNotEqual(hash(product1), hash(product2))

if __name__ == "__main__":
    unittest.main()
