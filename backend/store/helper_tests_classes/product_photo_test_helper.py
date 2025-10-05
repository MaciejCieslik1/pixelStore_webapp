from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.models import ProductPhoto, User


class ProductPhotoTestHelper:
    @staticmethod
    def create_product_photo(seller: User) -> ProductPhoto:
        product = ProductTestHelper.create_product(seller)
        product_photo = ProductPhoto(product=product, image_url="example_url", is_main_photo=True)
        product_photo.save()
        return product_photo
