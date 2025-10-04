from django.core.paginator import Paginator

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Product
from store.output_serializers.product_output_serializer import ProductOutputSerializer


class FindByIdProductService:
    def find_by_id(self, token: str, user: User, product_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)
        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            raise InvalidInputData("Product with this id does not exist.")

        serializer = ProductOutputSerializer(product)
        return serializer.data


class FindAllProductsService:
    def find_all(self, token: str, user: User, validated_data: dict) -> list[dict]:
        TokenUtils.verify_access_token(token, user)

        owner_username = validated_data.get("owner_username")
        name = validated_data.get("name")
        min_price = validated_data.get("min_price")
        max_price = validated_data.get("max_price")
        status = validated_data.get("status")
        ordering_field = validated_data.get("ordering_field") or "name"
        order = validated_data.get("order") or "asc"
        page = validated_data.get("page") or 1
        page_size = validated_data.get("page_size") or 10

        if not User.objects.filter(username=owner_username).exists():
            raise InvalidInputData("Product from seller with provided username does not exist.")

        products = Product.objects.all()

        if owner_username:
            products = products.filter(owner__username=owner_username)
        if name:
            products = products.filter(name__icontains=name)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if status:
            products = products.filter(status=status)

        if order == "desc":
            products = products.order_by(f"-{ordering_field}")
        else:
            products = products.order_by(ordering_field)

        response = [ProductOutputSerializer(product).data for product in products]

        paginator = Paginator(response, page_size)
        page_obj = paginator.get_page(page)

        return page_obj.object_list


class CreateProductService:
    def create(self, token: str, user: User, new_product_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        product = Product(owner=user, name=new_product_data["name"], description=new_product_data["description"],
            price=new_product_data["price"], amount=new_product_data["amount"], color=new_product_data["color"],
            weight=new_product_data["weight"], length=new_product_data["weight"], width=new_product_data["width"],
            height=new_product_data["height"], guarantee_period=new_product_data["guarantee_period"], status=new_product_data["status"])
        product.save()
        return "Product created successfully."

class UpdateProductService:
    def update(self, token : str, user: User, product_id: int) -> str:
        TokenUtils.verify_access_token(token, user)

        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            raise InvalidInputData("Product with this id does not exist.")
        if product.owner.username != user.username:
            raise InvalidInputData("Product does not belong to the user.")
        if product.status.lower() == "available":
            product.status = "unavailable"
        elif product.status.lower() == "unavailable":
            product.status = "archived"
        product.save()

        return "Product updated successfully."


class DeleteProductService:
    def delete(self, token : str, user: User, product_id: int) -> str:
        TokenUtils.verify_access_token(token, user)

        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            raise InvalidInputData("Product with this id does not exist.")
        if product.owner.username != user.username:
            raise InvalidInputData("Product does not belong to the user.")

        product.delete()

        return "Product deleted successfully."
