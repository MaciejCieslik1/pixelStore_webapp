import unittest
from datetime import datetime

from store.models import User, Product, ProductReview


class TestTransactionModel(unittest.TestCase):
    def setUp(self):
        self.owner = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                          bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.product = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)
        self.now = datetime.now()

    def test_eq_same_data(self):
        product_review1 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)
        product_review2 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)

        self.assertEqual(product_review1, product_review2)

    def test_eq_different_data(self):
        product_review1 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)
        product_review2 = ProductReview(product=self.product, rating=4, description="great", reviewer=self.owner,
                                        review_date=self.now)

        self.assertNotEqual(product_review1, product_review2)

    def test_hash_same_data(self):
        product_review1 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)
        product_review2 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)

        self.assertEqual(hash(product_review1), hash(product_review2))

    def test_hash_different_data(self):
        product_review1 = ProductReview(product=self.product, rating=5, description="great", reviewer=self.owner,
                                        review_date=self.now)
        product_review2 = ProductReview(product=self.product, rating=4, description="great", reviewer=self.owner,
                                        review_date=self.now)

        self.assertNotEquals(hash(product_review1), hash(product_review2))
