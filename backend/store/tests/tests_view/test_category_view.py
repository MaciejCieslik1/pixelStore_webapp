from unittest.mock import patch

import pytest
from django.db import DatabaseError
from rest_framework import status

from store.exceptions import TokenExpiredByReplacementError, CannotGetTokenFromRequestError, TokenExpiredError, \
    IncorrectTokenError, CategoryNameAlreadyOccupiedError, CategoryNotFoundError
from store.helper_tests_classes.authentication_test_helper import create_api_client_with_user
from store.helper_tests_classes.category_test_helper import CategoryTestHelper


@pytest.mark.django_db
class TestFindCategoryByName:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.category1, self.category_2 = CategoryTestHelper.create_categories()

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_success(self, mock_find_category_by_name):
        mock_find_category_by_name.return_value = {"name": "example_name1", "description": "example_description1"}

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "example_name1"
        assert response.data["description"] == "example_description1"
        mock_find_category_by_name.assert_called_once()

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_invalid_token(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_expired_token(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_cannot_get_token_from_request(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_token_expired_by_replacement(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_invalid_name(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = CategoryNotFoundError("Category name not found.")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Category name not found."

    @patch("store.service.category_service.FindCategoryByNameService.find_by_name")
    def test_find_category_by_name_other_exception(self, mock_find_category_by_name):
        mock_find_category_by_name.side_effect = DatabaseError("DB connection failed")

        response = self.client.get("/category/find_by_name/example_name1/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_find_category_by_name_serializer_error(self):
        response = self.client.get("/category/find_by_name/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFindAllCategories:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.category1, self.category2 = CategoryTestHelper.create_categories()

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_success(self, mock_find_all_categories):
        mock_find_all_categories.return_value = [{"name": "example_name1", "description": "example_description1"},
                                                 {"name": "example_name2", "description": "example_description2"}]

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["name"] == "example_name1"
        assert response.data[0]["description"] == "example_description1"
        assert response.data[1]["name"] == "example_name2"
        assert response.data[1]["description"] == "example_description2"
        mock_find_all_categories.assert_called_once()

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_invalid_token(self, mock_find_all_categories):
        mock_find_all_categories.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_expired_token(self, mock_find_all_categories):
        mock_find_all_categories.side_effect = TokenExpiredError("Access token error.")

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_cannot_get_token_from_request(self, mock_find_all_categories):
        mock_find_all_categories.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_token_expired_by_replacement(self, mock_find_all_categories):
        mock_find_all_categories.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.FindAllCategoriesService.find_all")
    def test_find_all_categories_other_exception(self, mock_find_all_categories):
        mock_find_all_categories.side_effect = DatabaseError("DB connection failed")

        response = self.client.get("/category/find_all/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."


@pytest.mark.django_db
class TestCreateCategoryByName:
    def setup_method(self):
        self.client, self.user = create_api_client_with_user()
        self.new_category_data = {"name": "example_name1", "description": "example_description1"}

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_success(self, mock_create_category):
        mock_create_category.return_value = "Category created successfully."

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["msg"] == "Category created successfully."
        mock_create_category.assert_called_once()

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_invalid_token(self, mock_create_category):
        mock_create_category.side_effect = IncorrectTokenError("Access token error.")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_expired_token(self, mock_create_category):
        mock_create_category.side_effect = TokenExpiredError("Access token error.")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_cannot_get_token_from_request(self, mock_create_category):
        mock_create_category.side_effect = CannotGetTokenFromRequestError("Access token error.")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_token_expired_by_replacement(self, mock_create_category):
        mock_create_category.side_effect = TokenExpiredByReplacementError("Access token error.")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["error"] == "Access token error."

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_name_already_occupied(self, mock_create_category):
        mock_create_category.side_effect = CategoryNameAlreadyOccupiedError("Category name is already occupied.")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data["error"] == "Category name is already occupied."

    @patch("store.service.category_service.CreateCategoryService.create")
    def test_create_category_other_exception(self, mock_create_category):
        mock_create_category.side_effect = DatabaseError("DB connection failed")

        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["error"] == "Unexpected error."

    def test_create_category_serializer_error(self):
        self.new_category_data["name"] = ""
        response = self.client.post("/category/create/", self.new_category_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
