from django.db import transaction
from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, OrderProduct, Product, Transaction
from store.output_serializers.order_product_output_serializer import OrderProductOutputSerializer


class FindByIdOrderProductService:
    def find_by_id(self, token: str, user: User, order_product_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)
        order_product = OrderProduct.objects.filter(pk=order_product_id).first()
        if order_product is None:
            raise InvalidInputData("Order with provided id does not exist.")
        if order_product.transaction.buyer != user:
            raise InvalidInputData("Transaction in which order exists does not belong to the user.")

        serializer = OrderProductOutputSerializer(order_product)
        return serializer.data


class CreateOrderProductService:
    def create(self, token: str, user: User, new_order_product_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)
        seller_username = new_order_product_data["seller_username"]
        seller = User.objects.filter(username=seller_username).first()
        if seller is None:
            raise InvalidInputData("Invalid seller username provided.")
        if seller_username == user.username:
            raise InvalidInputData("Cannot sell product to yourself.")

        product = Product.objects.filter(product_id=new_order_product_data["product_id"]).first()
        if product is None:
            raise InvalidInputData("Invalid product id provided.")
        if product.owner.username != seller_username:
            raise InvalidInputData("Seller is not the owner of this product.")
        if product.status == "unavailable":
            raise InvalidInputData("Product is unavailable.")
        if product.status == "archived":
            raise InvalidInputData("Product is archived.")

        transaction_obj = Transaction.objects.filter(transaction_id=new_order_product_data["transaction_id"]).first()
        if transaction_obj is None:
            raise InvalidInputData("Invalid transaction id provided.")
        if transaction_obj.buyer != user:
            raise InvalidInputData("Transaction in which order exists does not belong to the user.")
        if transaction_obj.is_finished:
            raise InvalidInputData("Cannot assign order to finished transaction.")

        with transaction.atomic():
            item_price = new_order_product_data["shopping_price"]
            order_product = OrderProduct(product=product, transaction=transaction_obj, seller=seller, shopping_price=item_price)
            order_product.save()

            product.status = "unavailable"
            product.save()

        return "Order created successfully."


class DeleteOrderProductService:
    def delete(self, token : str, user: User, order_product_id: int) -> str:
        TokenUtils.verify_access_token(token, user)
        order_product = OrderProduct.objects.filter(order_product_id=order_product_id).first()
        if order_product is None:
            raise InvalidInputData("Order with provided id does not exist.")
        if order_product.transaction.buyer != user:
            raise InvalidInputData("Transaction in which order exists does not belong to the user.")
        product = order_product.product

        with transaction.atomic():
            order_product.delete()
            product.status = "available"
            product.save()
        return "Order deleted successfully"
