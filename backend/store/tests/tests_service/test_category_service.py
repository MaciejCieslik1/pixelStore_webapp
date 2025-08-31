from datetime import timedelta
from django.utils import timezone

import pytest

from store.exceptions import TokenExpiredError, CategoryNotFoundError, TokenExpiredByReplacementError, \
    IncorrectTokenError, CategoryNameAlreadyOccupiedError
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper, TokenTestsHelper
from store.helper_tests_classes.category_test_helper import CategoryTestHelper
from store.models import User, Category
from store.service.category_service import FindCategoryByNameService, FindAllCategoriesService, CreateCategoryService


@pytest.mark.django_db
class TestFindCategoryByNameService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.categories_data = [{"name": "example_name1", "description": "example_description1"},
                                {"name": "example_name2", "description": "example_description2"}]
        CategoryTestHelper.create_categories()
        self.user = User.objects.get(username="tester")
        self.service = FindCategoryByNameService()

    def test_find_by_name(self):
        categories_before = Category.objects.count()
        result = self.service.find_by_name(self.token, self.user, self.categories_data[0]["name"])
        categories_after = Category.objects.count()

        assert self.categories_data[0] == result
        assert categories_before == categories_after

    def test_find_by_name_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_by_name(access_token, self.user, self.categories_data[0]["name"])
        categories_after = Category.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert categories_before == categories_after

    def test_find_by_name_incorrect_access_token(self):
        access_token = "invalid token"
        categories_before = Category.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_by_name(access_token, self.user, self.categories_data[0]["name"])
        categories_after = Category.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert categories_before == categories_after

    def test_find_by_name_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_by_name(access_token_first, user, self.categories_data[0]["name"])
        categories_after = Category.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert categories_before == categories_after

    def test_find_by_name_incorrect_name(self):
        categories_before = Category.objects.count()

        with pytest.raises(CategoryNotFoundError) as e:
            self.service.find_by_name(self.token, self.user, "invalid category")
        categories_after = Category.objects.count()

        assert f"Category with this name not found." in str(e.value)
        assert categories_before == categories_after


@pytest.mark.django_db
class TestFindAllCategories:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.categories_data = [{"name": "example_name1", "description": "example_description1"},
                                {"name": "example_name2", "description": "example_description2"}]
        CategoryTestHelper.create_categories()
        self.user = User.objects.get(username="tester")
        self.service = FindAllCategoriesService()

    def test_find_all(self):
        categories_before = Category.objects.count()
        result = self.service.find_all(self.token, self.user)
        categories_after = Category.objects.count()

        assert self.categories_data == result
        assert categories_before == categories_after

    def test_find_all_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.find_all(access_token, self.user)
        categories_after = Category.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert categories_before == categories_after

    def test_find_all_incorrect_access_token(self):
        access_token = "invalid token"
        categories_before = Category.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.find_all(access_token, self.user)
        categories_after = Category.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert categories_before == categories_after

    def test_find_all_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.find_all(access_token_first, user)
        categories_after = Category.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert categories_before == categories_after


@pytest.mark.django_db
class TestCreateCategoryService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.category_data = {"name": "example_name1", "description": "example_description1"}
        category = Category(name=self.category_data["name"], description=self.category_data["description"])
        category.save()
        self.user = User.objects.get(username="tester")
        self.service = CreateCategoryService()

    def test_create(self):
        self.category_data2 = {"name": "example_name2", "description": "example_description2"}
        categories_before = Category.objects.count()
        result = self.service.create(self.token, self.user, self.category_data2)
        categories_after = Category.objects.count()

        assert result == f"Category {self.category_data2['name']} created successfully."
        assert categories_after == categories_before + 1

    def test_create_expired_access_token(self):
        access_token = TokenTestsHelper.generate_access_token(self.user.user_id,"access",
                        timezone.now() - timedelta(days=1), timezone.now() - timedelta(days=2),
                                                              token_version=1)
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredError) as e:
            self.service.create(access_token, self.user, self.category_data)
        categories_after = Category.objects.count()

        assert f"Access token has expired." in str(e.value)
        assert categories_before == categories_after

    def test_create_incorrect_access_token(self):
        access_token = "invalid token"
        categories_before = Category.objects.count()

        with pytest.raises(IncorrectTokenError) as e:
            self.service.create(access_token, self.user, self.category_data)
        categories_after = Category.objects.count()

        assert f"Incorrect access token." in str(e.value)
        assert categories_before == categories_after

    def test_create_expired_by_replacement_access_token(self):
        access_token_first = self.token
        AuthenticationHelper.login_user(self.user_data)
        user = User.objects.get(username="tester")
        categories_before = Category.objects.count()

        with pytest.raises(TokenExpiredByReplacementError) as e:
            self.service.create(access_token_first, user, self.category_data)
        categories_after = Category.objects.count()

        assert f"Access token is no longer valid." in str(e.value)
        assert categories_before == categories_after

    def test_create_name_already_occupied(self):
        AuthenticationHelper.login_user(self.user_data)
        categories_before = Category.objects.count()

        with pytest.raises(CategoryNameAlreadyOccupiedError) as e:
            self.service.create(self.token, self.user, self.category_data)
        categories_after = Category.objects.count()

        assert f"Category with this name already exists." in str(e.value)
        assert categories_before == categories_after
