from decimal import Decimal

from django.utils import timezone

from store.exceptions import NotEnoughFundsError
from store.models import OrderProduct, Notification


class PaymentHelper:
    @staticmethod
    def make_payment(order_product: OrderProduct, is_return: bool = False) -> None:
        order_product_id = order_product.order_product_id
        buyer = order_product.transaction.buyer
        seller = order_product.seller
        price = order_product.shopping_price
        buyer_money_casted = int(buyer.money * 100)
        seller_money_casted = int(seller.money * 100)
        price_casted = int(price * 100)
        if is_return:
            buyer_money_casted += price_casted
            seller_money_casted -= price_casted
            if seller_money_casted < 0:
                raise NotEnoughFundsError("Seller has no enough money to proceed the payment")
            text_buyer = f"Incoming founds: {price}. Return from order product id: {order_product_id}."
            text_seller = f"Outgoing founds: {price}. Return from order product id: {order_product_id}."
            notification_buyer = Notification(sender=seller, receiver=buyer, sent_date_time=timezone.now(), text=text_buyer)
            notification_buyer.save()
        else:
            buyer_money_casted -= price_casted
            seller_money_casted += price_casted
            if buyer_money_casted < 0:
                raise NotEnoughFundsError("Buyer has no enough money to proceed the payment")
            text_seller = f"Incoming founds: {price}. Order product id: {order_product_id}."
        buyer.money = Decimal(buyer_money_casted) / Decimal(100)
        seller.money = Decimal(seller_money_casted) / Decimal(100)
        buyer.save()
        seller.save()

        notification_seller = Notification(sender=buyer, receiver=seller, sent_date_time=timezone.now(), text=text_seller)
        notification_seller.save()
