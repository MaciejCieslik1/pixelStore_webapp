from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, ProductPhoto, Product
from store.output_serializers.product_photo_output_serializer import ProductPhotoOutputSerializer


class FindByIdProductPhotoService:
    def find_by_id(self, token: str, user: User, product_photo_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)

        product_photo = ProductPhoto.objects.filter(pk=product_photo_id).first()
        if product_photo is None:
            raise InvalidInputData("Product photo with this id does not exist.")

        serializer = ProductPhotoOutputSerializer(product_photo)
        return serializer.data


class FindAllForProductService:
    def find_all_for_product(self, token: str, user: User, product_id: int) -> list[dict]:
        TokenUtils.verify_access_token(token, user)

        if not Product.objects.filter(pk=product_id).exists():
            raise InvalidInputData("Product with this id does not exist.")

        product_photos = ProductPhoto.objects.filter(product_id=product_id).order_by('product_photo_id')

        serializer = ProductPhotoOutputSerializer(product_photos, many=True)
        return serializer.data


class FindMainPhotoProductPhotoService:
    def find_main_photo(self, token: str, user: User, product_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)

        if not Product.objects.filter(pk=product_id).exists():
            raise InvalidInputData("Product with this id does not exist.")

        product_photo = ProductPhoto.objects.filter(product_id=product_id, is_main_photo=True).first()

        serializer = ProductPhotoOutputSerializer(product_photo)
        return serializer.data


class CreateProductPhotoService:
    def create(self, token: str, user: User, new_product_photo_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        if not Product.objects.filter(product_id=new_product_photo_data["product_id"]).exists():
            raise InvalidInputData("Product with this id does not exist.")

        product = Product.objects.get(product_id=new_product_photo_data["product_id"])
        if product.owner.username != user.username:
            raise InvalidInputData("Product with this id does not belong to the user.")

        if new_product_photo_data["is_main_photo"]:
            old_main_product_photo = ProductPhoto.objects.filter(
                product_id=new_product_photo_data["product_id"], is_main_photo=True).first()

            if old_main_product_photo is not None:
                old_main_product_photo.is_main_photo = False
                old_main_product_photo.save()

        product_photo = ProductPhoto(product=product, image_url=new_product_photo_data["image_url"],
            is_main_photo=new_product_photo_data["is_main_photo"])
        product_photo.save()
        return "Product photo created successfully."


class DeleteProductPhotoService:
    def delete(self, token : str, user: User, product_photo_id: int) -> str:
        TokenUtils.verify_access_token(token, user)

        product_photo = ProductPhoto.objects.filter(product_photo_id=product_photo_id).first()
        if not product_photo:
            raise InvalidInputData("Product photo with this id does not exist.")

        product = product_photo.product
        if product.owner.username != user.username:
            raise InvalidInputData("Product photo with this id does not belong to the user.")

        product_photo.delete()
        return "Product photo deleted successfully."
