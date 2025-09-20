import pytest
from django.utils import timezone

from store.exceptions import NotEnoughFundsError
from store.helper_classes.payment_helper import PaymentHelper
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.models import User, Transaction, Product, OrderProduct, Notification


@pytest.mark.django_db
class TestPaymentHelper:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller_data = AuthenticationHelper.return_exemplary_user_data()
        self.seller_data["email"] = "seller@example.com"
        self.seller_data["username"] = "seller"
        self.token = AuthenticationHelper.register_and_login_user(self.seller_data)
        self.seller = User.objects.get(username=self.seller_data["username"])
        transaction = Transaction(buyer=self.user, total_price=1000, date_time=timezone.now(), is_finished=False)
        transaction.save()
        product = Product.objects.create(owner=self.seller, name="cpu", description="example", price=1000, amount=10,
            color="black", weight=0.45, length=15.00, width=15.00, height=0.80, guarantee_period=24, status="AVAILABLE")
        product.save()
        self.order_product = OrderProduct(transaction=transaction, product=product, seller=self.seller, shopping_price=1000)
        self.order_product.save()
        self.price = self.order_product.shopping_price
        self.payment_helper = PaymentHelper()

    def test_payment_success(self):
        self.user.money = 10000
        self.user.save()
        user_money_before = self.user.money
        seller_money_before = self.seller.money
        notifications_before = Notification.objects.count()

        self.payment_helper.make_payment(self.order_product, False)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller = User.objects.get(username=self.seller_data["username"])
        user_money_after = self.user.money
        seller_money_after = self.seller.money
        notifications_after = Notification.objects.count()

        assert notifications_before == notifications_after - 1
        assert user_money_before == user_money_after + self.price
        assert seller_money_before == seller_money_after - self.price

    def test_payment_return_success(self):
        self.seller.money = 10000
        self.seller.save()
        user_money_before = self.user.money
        seller_money_before = self.seller.money
        notifications_before = Notification.objects.count()

        self.payment_helper.make_payment(self.order_product, True)
        self.user = User.objects.get(username=self.user_data["username"])
        self.seller = User.objects.get(username=self.seller_data["username"])
        user_money_after = self.user.money
        seller_money_after = self.seller.money
        notifications_after = Notification.objects.count()

        assert notifications_before == notifications_after - 2
        assert user_money_before == user_money_after - self.price
        assert seller_money_before == seller_money_after + self.price

    def test_payment_buyer_too_little_money(self):
        user_money_before = self.user.money
        seller_money_before = self.seller.money
        notifications_before = Notification.objects.count()

        with pytest.raises(NotEnoughFundsError) as e:
            self.payment_helper.make_payment(self.order_product, False)

        self.user = User.objects.get(username=self.user_data["username"])
        self.seller = User.objects.get(username=self.seller_data["username"])
        user_money_after = self.user.money
        seller_money_after = self.seller.money
        notifications_after = Notification.objects.count()

        assert f"Buyer has no enough money to proceed the payment" in str(e.value)
        assert notifications_before == notifications_after
        assert user_money_before == user_money_after
        assert seller_money_before == seller_money_after

    def test_payment_return_seller_too_little_money(self):
        user_money_before = self.user.money
        seller_money_before = self.seller.money
        notifications_before = Notification.objects.count()

        with pytest.raises(NotEnoughFundsError) as e:
            self.payment_helper.make_payment(self.order_product, True)

        self.user = User.objects.get(username=self.user_data["username"])
        self.seller = User.objects.get(username=self.seller_data["username"])
        user_money_after = self.user.money
        seller_money_after = self.seller.money
        notifications_after = Notification.objects.count()

        assert f"Seller has no enough money to proceed the payment" in str(e.value)
        assert notifications_before == notifications_after
        assert user_money_before == user_money_after
        assert seller_money_before == seller_money_after
