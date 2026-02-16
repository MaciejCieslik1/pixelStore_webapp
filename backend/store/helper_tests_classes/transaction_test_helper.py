from django.utils import timezone
from decimal import Decimal

from store.models import User, Transaction


class TransactionTestHelper:
    @staticmethod
    def create_transaction(buyer: User) -> Transaction:
        transaction = Transaction(buyer=buyer, total_price=Decimal('1'), date_time=timezone.now(),
                                  is_finished=False)
        transaction.save()
        return transaction
