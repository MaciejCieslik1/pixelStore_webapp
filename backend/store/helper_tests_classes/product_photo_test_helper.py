from store.models import ProductPhoto, Product


class ProductPhotoTestHelper:
    @staticmethod
    def create_product_photo(product: Product, image_url: str) -> ProductPhoto:
        product_photo = ProductPhoto(product=product, image_url=image_url, is_main_photo=True)
        product_photo.save()
        return product_photo
