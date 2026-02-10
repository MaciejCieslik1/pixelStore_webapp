import datetime

from django.core.paginator import Paginator

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, ProductReview, Product
from store.output_serializers.product_review_output_serializer import ProductReviewOutputSerializer


class FindByIdProductReviewService:
    def find_by_id(self, token: str, user: User, product_review_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)
        product_review = ProductReview.objects.filter(pk=product_review_id).first()
        if product_review is None:
            raise InvalidInputData("Product review with this id does not exist.")

        serializer = ProductReviewOutputSerializer(product_review)
        return serializer.data


class FindAllProductReviewsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        TokenUtils.verify_access_token(token, user)

        product_id = validated_data.get("product_id")
        page = validated_data.get("page") or 1
        page_size = validated_data.get("page_size") or 10

        if not Product.objects.filter(product_id=product_id).exists():
            raise InvalidInputData("Product with this id does not exist.")

        product_reviews = ProductReview.objects.filter(product__product_id=product_id)

        response = [ProductReviewOutputSerializer(product).data for product in product_reviews]

        paginator = Paginator(response, page_size)
        page_obj = paginator.get_page(page)

        return page_obj.object_list


class FindAllFromUserProductReviewsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        TokenUtils.verify_access_token(token, user)

        reviewer_username = validated_data.get("reviewer_username")
        page = validated_data.get("page") or 1
        page_size = validated_data.get("page_size") or 10

        product_reviews = ProductReview.objects.filter(reviewer__username=reviewer_username)

        response = [ProductReviewOutputSerializer(product).data for product in product_reviews]

        paginator = Paginator(response, page_size)
        page_obj = paginator.get_page(page)

        return page_obj.object_list


class CreateProductReviewService:
    def create(self, token: str, user: User, new_product_review_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        product = Product.objects.filter(pk=new_product_review_data["product_id"]).first()
        if product is None:
            raise InvalidInputData("Product with this id does not exist.")
        if product.owner.username == user.username:
            raise InvalidInputData("Product with this id belongs to the user.")

        product_review = ProductReview(product=product, rating=new_product_review_data["rating"],
            description=new_product_review_data["description"], reviewer=user, review_date=datetime.datetime.now())
        product_review.save()

        return "Product review created successfully."

class DeleteProductReviewService:
    def delete(self, token : str, user: User, product_review_id: int) -> str:
        TokenUtils.verify_access_token(token, user)

        product_review = ProductReview.objects.filter(pk=product_review_id).first()
        if product_review is None:
            raise InvalidInputData("Product review with this id does not exist.")
        if product_review.reviewer.username != user.username:
            raise InvalidInputData("Product review with this id does not belong to the user.")

        product_review.delete()

        return "Product review deleted successfully."
