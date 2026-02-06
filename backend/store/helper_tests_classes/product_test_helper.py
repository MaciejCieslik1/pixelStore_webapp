from store.models import User, Product


class ProductTestHelper:
    @staticmethod
    def create_product(seller: User) -> Product:
        product = Product(owner=seller, name="cpu", description="example", price=1000, amount=10, color="black",
                            weight=0.45, length=15.0, width=15.0, height=0.8, guarantee_period=24, status="AVAILABLE")
        product.save()
        return product