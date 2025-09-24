from store.models import User, Product


class ProductTestHelper:
    @staticmethod
    def create_product(seller: User):
        product = Product(owner=seller, name="cpu", description="example", price=1000, amount=10, color="black",
                            weight=0.45, length=15.00, width=15.00, height=0.80, guarantee_period=24, status="AVAILABLE")
        product.save()
        return product