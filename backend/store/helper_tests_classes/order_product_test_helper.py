from django.utils import timezone

from store.models import OrderProduct, Transaction, User, Product


class OrderProductTestHelper:
    @staticmethod
    def create_order_products(user: User) -> OrderProduct:
        transaction = Transaction(buyer=user, total_price=1000, date_time = timezone.now(), is_finished = False)
        transaction.save()
        seller_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
         "is_verified": False, "bio": "I'm new here!", "money": 100000.00, "is_superuser": False,
         "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw", "country": "Poland"}
        seller = User.create_user(seller_data)
        seller.save()
        product = Product.objects.create(owner=seller, name="cpu", description="example", price=1000, amount=10, color="black",
            weight=0.45, length=15.00, width=15.00, height=0.80, guarantee_period=24, status="AVAILABLE")
        product.save()
        order_product = OrderProduct(transaction=transaction, product=product, seller=seller, shopping_price=1000)
        order_product.save()
        return order_product

