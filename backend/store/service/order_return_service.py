from django.utils import timezone

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.helper_classes.payment_helper import PaymentHelper
from store.models import User, OrderReturn, OrderProduct, Notification
from store.output_serializers.order_return_output_serializer import OrderReturnOutputSerializer


class FindByIdOrderReturnService:
    def find_by_id(self, token: str, user: User, order_return_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)
        order_return = OrderReturn.objects.filter(pk=order_return_id).first()
        if order_return is None:
            raise InvalidInputData("Order return with provided id does not exist.")
        if order_return.order_product.transaction.buyer != user and order_return.order_product.seller != user:
            raise InvalidInputData("Transaction in which order exists does not belong to the user.")

        serializer = OrderReturnOutputSerializer(order_return)
        return serializer.data


class CreateOrderReturnService:
    def create(self, token: str, user: User, new_order_return_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)
        order_product_id = new_order_return_data["order_product_id"]
        description = new_order_return_data["description"]
        order_product = OrderProduct.objects.filter(pk=order_product_id).first()
        if order_product is None:
            raise InvalidInputData("Order with provided id does not exist.")
        if order_product.transaction.buyer != user:
            raise InvalidInputData("Transaction in which order exists does not belong to the user.")

        order_return = OrderReturn(order_product=order_product, description=description, return_date_time=timezone.now(),
            is_accepted=False)
        order_return.save()

        text = f"User: {user.username} wants to return his/her order. Order return id is: {order_return.id}."
        notification = Notification(sender=user, receiver=order_product.seller, sent_date_time=timezone.now(), text=text)
        notification.save()

        return "Order return created successfully."


class UpdateOrderReturnService:
    def update(self, token : str, user: User, order_return_id: int) -> str:
        TokenUtils.verify_access_token(token, user)
        order_return = OrderReturn.objects.filter(pk=order_return_id).first()
        if order_return is None:
            raise InvalidInputData("Order return with provided id does not exist.")
        if order_return.order_product.seller != user:
            raise InvalidInputData("User is not seller of the product.")

        order_return.is_accepted = True
        order_return.save()

        order_product = order_return.order_product
        buyer = order_product.transaction.buyer

        text = f"Seller: {user.username} accepted your return request. Order return id is: {order_return.order_return_id}."
        notification = Notification(sender=user, receiver=buyer, sent_date_time=timezone.now(), text=text)
        notification.save()

        PaymentHelper.make_payment(order_product, is_return=True)

        return "Order return updated successfully."
