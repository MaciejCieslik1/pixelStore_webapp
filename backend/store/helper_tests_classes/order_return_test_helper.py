from django.utils import timezone

from store.helper_tests_classes.order_product_test_helper import OrderProductTestHelper
from store.models import User, OrderReturn


class OrderReturnTestHelper:
    @staticmethod
    def create_order_return(user: User) -> OrderReturn:
        order_product = OrderProductTestHelper.create_order_products(user)
        order_return = OrderReturn(order_product=order_product, description="example_description", return_date_time=timezone.now(),
            is_accepted=False)
        order_return.save()
        return order_return
