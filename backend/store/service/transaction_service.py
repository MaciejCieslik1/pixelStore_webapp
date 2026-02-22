import datetime

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from store.exceptions import InvalidInputData
from store.helper_classes.authentication_helper import TokenUtils
from store.models import User, Transaction, OrderProduct, UserStatistics
from store.output_serializers.transaction_output_serializer import TransactionOutputSerializer


class FindByIdTransactionService:
    def find_by_id(self, token: str, user: User, transaction_id: int) -> dict:
        TokenUtils.verify_access_token(token, user)

        transaction = Transaction.objects.filter(pk=transaction_id).first()
        if transaction is None:
            raise InvalidInputData("Transaction with this id does not exist.")

        if transaction.buyer.username != user.username:
            order_product = OrderProduct.objects.filter(transaction__transaction_id=transaction_id).first()
            if order_product.seller.username != user.username:
                raise InvalidInputData("Transaction with this id does not belong to the user.")

        serializer = TransactionOutputSerializer(transaction)
        return serializer.data


class FindAllMineTransactionsService:
    def find_all_mine(self, token: str, user: User, validated_data: dict) -> list[dict]:
        TokenUtils.verify_access_token(token, user)

        page = validated_data.get("page") or 1
        page_size = validated_data.get("page_size") or 10

        transactions = Transaction.objects.filter(
            Q(buyer=user) |
            Q(order_products__seller=user)
        ).distinct()

        response = [TransactionOutputSerializer(transaction).data for transaction in transactions]

        paginator = Paginator(response, page_size)
        page_obj = paginator.get_page(page)

        return page_obj.object_list


class CreateTransactionService:
    def create(self, token: str, user: User, new_transaction_data: dict) -> str:
        TokenUtils.verify_access_token(token, user)

        buyer = User.objects.filter(username=new_transaction_data["buyer_username"]).first()
        if buyer is None:
            raise InvalidInputData("User with this username does not exist.")

        transaction = Transaction(buyer=buyer, total_price=new_transaction_data["total_price"],
                                  date_time=datetime.datetime.now(), is_finished=False)
        transaction.save()
        return "Transaction created successfully."


class UpdateTransactionService:
    def update(self, token : str, user: User, transaction_id: int) -> str:
        TokenUtils.verify_access_token(token, user)

        transaction_obj = Transaction.objects.filter(pk=transaction_id).first()

        if transaction_obj is None:
            raise InvalidInputData("Transaction with this id does not exist.")
        if transaction_obj.buyer.username != user.username:
            raise InvalidInputData("Transaction with this id does not belong to the user.")
        if transaction_obj.is_finished:
            raise InvalidInputData("Transaction with this id is already finished.")
        if transaction_obj.buyer.money < transaction_obj.total_price:
            raise InvalidInputData("You do not have enough money.")

        with transaction.atomic():
            transaction_obj.is_finished = True
            transaction_obj.save()

            order_product = OrderProduct.objects.filter(transaction_id=transaction_id).first()
            seller = order_product.seller
            buyer = transaction_obj.buyer

            seller.money += transaction_obj.total_price
            buyer.money -= transaction_obj.total_price

            seller_statistics = UserStatistics.objects.filter(user=seller).first()
            buyer_statistics = UserStatistics.objects.filter(user=buyer).first()
            seller_statistics.products_sold += 1
            buyer_statistics.products_bought += 1
            seller_statistics.save()
            buyer_statistics.save()

            seller.save()
            buyer.save()

        return "Transaction updated successfully."
