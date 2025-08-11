import unittest
from store.models import User, Product, ProductPhoto


class TestProductPhotoModel(unittest.TestCase):
    def setUp(self):
        self.owner = User(email="sender@example.com", username="testuser1", password="hashedpwd", is_verified=False,
                          bio="I'm new here!", money=0.00, is_superuser=False, last_login=None, token_version=0)
        self.product = Product(owner=self.owner, name="cpu", description="dsfffefee", price=1000, amount=2,
                           color="red", weight=3, length=2, width=0.5, height=1.1, guarantee_period=4,
                           status=Product.ProductStatus.AVAILABLE)

    def test_eq_same_data(self):
        product_photo1 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)
        product_photo2 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)

        self.assertEqual(product_photo1, product_photo2)

    def test_eq_different_data(self):
        product_photo1 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)
        product_photo2 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=False)

        self.assertNotEqual(product_photo1, product_photo2)

    def test_hash_same_data(self):
        product_photo1 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)
        product_photo2 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)

        self.assertEqual(hash(product_photo1), hash(product_photo2))

    def test_hash_different_data(self):
        product_photo1 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=True)
        product_photo2 = ProductPhoto(product=self.product, image_url="dsfdsfdsds", is_main_photo=False)

        self.assertNotEqual(hash(product_photo1), hash(product_photo2))
