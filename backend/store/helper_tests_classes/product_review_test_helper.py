import datetime

from store.models import ProductReview, Product, User


class ProductReviewTestHelper:
    @staticmethod
    def create_product_review(product: Product, reviewer: User) -> ProductReview:
        product_review = ProductReview(product=product, rating=5.0, description="example", reviewer=reviewer,
                                       review_date=datetime.datetime.now())
        product_review.save()
        return product_review
