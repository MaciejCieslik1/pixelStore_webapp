import pytest

from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.helper_tests_classes.product_review_test_helper import ProductReviewTestHelper
from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.models import User, ProductPhoto, ProductReview
from store.service.product_review_service import FindByIdProductReviewService, FindAllProductReviewsService, \
    FindAllFromUserProductReviewsService, CreateProductReviewService, DeleteProductReviewService


@pytest.mark.django_db
class TestFindByIdProductReviewService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.product_review = ProductReviewTestHelper.create_product_review(product, self.owner)
        self.product_review_id = self.product_review.product_review_id
        self.product_review_dict = {
            "product_review_id": self.product_review_id,
            "product_id": str(self.product_review.product_id),
            "rating": str(self.product_review.rating),
            "description": self.product_review.description,
            "reviewer_username": self.product_review.reviewer.username,
            "review_date": str(self.product_review.review_date.strftime("%Y-%m-%d")),
        }
        self.service = FindByIdProductReviewService()


    def test_find_by_id(self):
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.find_by_id(self.token, self.owner, self.product_review_id)
        product_reviews_after = ProductReview.objects.all().count()

        assert result == self.product_review_dict
        assert product_reviews_before == product_reviews_after


    def test_find_by_id_invalid_id(self):
        product_reviews_before = ProductReview.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.owner, self.product_review_id + 10)
        product_reviews_after = ProductReview.objects.all().count()

        assert f"Product review with this id does not exist." in str(e.value)
        assert product_reviews_before == product_reviews_after


@pytest.mark.django_db
class TestFindAllForProductProductReviewService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product1 = ProductTestHelper.create_product(self.owner)
        product2 = ProductTestHelper.create_product(self.owner)
        self.product_review1 = ProductReviewTestHelper.create_product_review(product1, self.owner)
        self.product_review2 = ProductReviewTestHelper.create_product_review(product1, self.owner)
        self.product_review3 = ProductReviewTestHelper.create_product_review(product2, self.owner)
        self.product_review_dict1 = {
            "product_review_id": str(self.product_review1.product_review_id),
            "product_id": str(self.product_review1.product_id),
            "rating": str(self.product_review1.rating),
            "description": self.product_review1.description,
            "reviewer_username": self.product_review1.reviewer.username,
            "review_date": str(self.product_review1.review_date.strftime("%Y-%m-%d")),
        }
        self.product_review_dict2 = {
            "product_review_id": str(self.product_review2.product_review_id),
            "product_id": str(self.product_review2.product_id),
            "rating": str(self.product_review2.rating),
            "description": self.product_review2.description,
            "reviewer_username": self.product_review2.reviewer.username,
            "review_date": str(self.product_review2.review_date.strftime("%Y-%m-%d")),
        }
        self.product_review_dict3 = {
            "product_review_id": str(self.product_review3.product_review_id),
            "product_id": str(self.product_review3.product_id),
            "rating": str(self.product_review3.rating),
            "description": self.product_review3.description,
            "reviewer_username": self.product_review3.reviewer.username,
            "review_date": str(self.product_review3.review_date.strftime("%Y-%m-%d")),
        }
        self.product_reviews = [self.product_review_dict1, self.product_review_dict2]
        self.service = FindAllProductReviewsService()


    def test_find_all_for_product(self):
        product_review_find_data = {
            "product_id": self.product_review1.product_id,
            "page": 1,
            "page_size": 10,
        }
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.find_all(self.token, self.owner, product_review_find_data)
        product_reviews_after = ProductReview.objects.all().count()

        assert len(result) == len(self.product_reviews)
        assert product_reviews_before == product_reviews_after


    def test_find_all_for_product_invalid_product_id(self):
        product_review_find_data = {
            "product_id": self.product_review1.product_id + 10,
            "page": 1,
            "page_size": 10,
        }
        product_reviews_before = ProductReview.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_all(self.token, self.owner, product_review_find_data)
        product_reviews_after = ProductReview.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert product_reviews_before == product_reviews_after


@pytest.mark.django_db
class TestFindAllFromUserProductReviewService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.product_review1 = ProductReviewTestHelper.create_product_review(product, self.owner)
        self.product_review2 = ProductReviewTestHelper.create_product_review(product, self.owner)
        self.product_review_dict1 = {
            "product_review_id": self.product_review1.product_review_id,
            "product_id": str(self.product_review1.product_id),
            "rating": str(self.product_review1.rating),
            "description": self.product_review1.description,
            "reviewer_username": self.product_review1.reviewer.username,
            "review_date": str(self.product_review1.review_date.strftime("%Y-%m-%d")),
        }
        self.product_review_dict2 = {
            "product_review_id": self.product_review2.product_review_id,
            "product_id": str(self.product_review2.product_id),
            "rating": str(self.product_review2.rating),
            "description": self.product_review2.description,
            "reviewer_username": self.product_review2.reviewer.username,
            "review_date": self.product_review2.review_date.strftime("%Y-%m-%d"),
        }
        self.product_reviews = [self.product_review_dict1, self.product_review_dict2]
        self.service = FindAllFromUserProductReviewsService()


    def test_find_all_from_user(self):
        product_review_find_data = {
            "reviewer_username": self.product_review1.reviewer.username,
            "page": 1,
            "page_size": 10,
        }
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.find_all(self.token, self.owner, product_review_find_data)
        product_reviews_after = ProductReview.objects.all().count()

        assert len(result) == len(self.product_reviews)
        assert product_reviews_before == product_reviews_after


    def test_find_all_from_user_empty(self):
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["email"] = "test2@example.com"
        self.user_data2["username"] = "tester2"
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.user2 = User.objects.get(username=self.user_data2["username"])
        product_review_find_data = {
            "reviewer_username": self.user2,
            "page": 1,
            "page_size": 10,
        }
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.find_all(self.token, self.owner, product_review_find_data)
        product_reviews_after = ProductReview.objects.all().count()

        assert len(result) == 0
        assert product_reviews_before == product_reviews_after


@pytest.mark.django_db
class TestCreateProductReviewService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2 = AuthenticationHelper.return_exemplary_user_data()
        self.user_data2["email"] = "test2@example.com"
        self.user_data2["username"] = "tester2"
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        AuthenticationHelper.register_and_login_user(self.user_data2)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.user2 = User.objects.get(username=self.user_data2["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.create_product_review_dict = {
            "product_id": product.product_id,
            "rating": 5.0,
            "description": "example description",
        }
        self.service = CreateProductReviewService()


    def test_create(self):
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.create(self.token, self.user2, self.create_product_review_dict)
        product_reviews_after = ProductReview.objects.all().count()

        assert result == "Product review created successfully."
        assert product_reviews_before == product_reviews_after - 1


    def test_create_invalid_product_id(self):
        product_reviews_before = ProductReview.objects.all().count()
        self.create_product_review_dict["product_id"] += 10
        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.user2, self.create_product_review_dict)
        product_reviews_after = ProductReview.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert product_reviews_before == product_reviews_after


    def test_create_product_belongs_to_the_user(self):
        product_reviews_before = ProductReview.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.owner, self.create_product_review_dict)
        product_reviews_after = ProductPhoto.objects.all().count()

        assert f"Product with this id belongs to the user." in str(e.value)
        assert product_reviews_before == product_reviews_after


@pytest.mark.django_db
class TestDeleteProductReviewService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.product = ProductTestHelper.create_product(self.owner)
        self.product_review = ProductReviewTestHelper.create_product_review(self.product, self.owner)
        self.product_review_id = self.product_review.product_review_id
        self.service = DeleteProductReviewService()


    def test_delete(self):
        product_reviews_before = ProductReview.objects.all().count()
        result = self.service.delete(self.token, self.owner, self.product_review_id)
        product_reviews_after = ProductReview.objects.all().count()

        assert result == "Product review deleted successfully."
        assert product_reviews_before - 1 == product_reviews_after


    def test_delete_invalid_product_review_id(self):
        product_reviews_before = ProductReview.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, self.owner, self.product_review_id + 10)
        product_reviews_after = ProductReview.objects.all().count()

        assert f"Product review with this id does not exist." in str(e.value)
        assert product_reviews_before == product_reviews_after


    def test_delete_product_review_does_not_belong_to_the_user(self):
        product_reviews_before = ProductReview.objects.all().count()
        user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        AuthenticationHelper.register_and_login_user(user2_data)
        user2 = User.objects.get(username=user2_data["username"])

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, user2, self.product_review_id)
        product_reviews_after = ProductReview.objects.all().count()

        assert f"Product review with this id does not belong to the user." in str(e.value)
        assert product_reviews_before == product_reviews_after
