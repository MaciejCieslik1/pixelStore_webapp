import pytest

from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.helper_tests_classes.product_photo_test_helper import ProductPhotoTestHelper
from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.models import User, ProductPhoto
from store.service.product_photo_service import FindByIdProductPhotoService, FindAllForProductService, \
    FindMainPhotoProductPhotoService, CreateProductPhotoService, DeleteProductPhotoService


@pytest.mark.django_db
class TestFindByIdProductPhotoService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.product_photo = ProductPhotoTestHelper.create_product_photo(product, "path1")
        self.product_photo_id = self.product_photo.product_photo_id
        self.product_photo_dict = {
            "product_photo_id": self.product_photo_id,
            "image_url": self.product_photo.image_url,
            "is_main_photo": self.product_photo.is_main_photo,
        }
        self.service = FindByIdProductPhotoService()


    def test_find_by_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        result = self.service.find_by_id(self.token, self.owner, self.product_photo_id)
        product_photos_after = ProductPhoto.objects.all().count()

        assert result == self.product_photo_dict
        assert product_photos_before == product_photos_after


    def test_find_by_id_invalid_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.owner, self.product_photo_id + 10)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product photo with this id does not exist." in str(e.value)
        assert product_photos_before == product_photos_after


@pytest.mark.django_db
class TestFindAllForProductProductPhotoService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.product_photo1 = ProductPhotoTestHelper.create_product_photo(product, "path1")
        self.product_photo2 = ProductPhotoTestHelper.create_product_photo(product, "path2")
        self.product_photo_dict1 = {
            "product_photo_id": self.product_photo1.product_photo_id,
            "image_url": self.product_photo1.image_url,
            "is_main_photo": self.product_photo1.is_main_photo,
        }
        self.product_photo_dict2 = {
            "product_photo_id": self.product_photo2.product_photo_id,
            "image_url": self.product_photo2.image_url,
            "is_main_photo": self.product_photo2.is_main_photo,
        }
        self.product_photos = [self.product_photo_dict1, self.product_photo_dict2]
        self.service = FindAllForProductService()


    def test_find_all_for_product(self):
        product_photos_before = ProductPhoto.objects.all().count()
        result = self.service.find_all_for_product(self.token, self.owner, self.product_photo1.product_id)
        product_photos_after = ProductPhoto.objects.all().count()

        assert len(result) == len(self.product_photos)
        assert product_photos_before == product_photos_after


    def test_find_all_for_product_invalid_product_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_all_for_product(self.token, self.owner, self.product_photo1.product_id + 10)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert product_photos_before == product_photos_after


@pytest.mark.django_db
class TestFindMainPhotoProductPhotoService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.product_photo1 = ProductPhotoTestHelper.create_product_photo(product, "path1")
        self.product_photo2 = ProductPhotoTestHelper.create_product_photo(product, "path2")
        self.product_photo_dict1 = {
            "product_photo_id": self.product_photo1.product_photo_id,
            "image_url": self.product_photo1.image_url,
            "is_main_photo": True,
        }
        self.product_photo_dict2 = {
            "product_photo_id": self.product_photo2.product_photo_id,
            "image_url": self.product_photo2.image_url,
            "is_main_photo": False,
        }
        self.product_photos = [self.product_photo1, self.product_photo2]
        self.service = FindMainPhotoProductPhotoService()


    def test_find_main_photo(self):
        product_photos_before = ProductPhoto.objects.all().count()
        result = self.service.find_main_photo(self.token, self.owner, self.product_photo1.product_id)
        product_photos_after = ProductPhoto.objects.all().count()

        assert result == self.product_photo_dict1
        assert product_photos_before == product_photos_after


    def test_find_main_photo_invalid_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_main_photo(self.token, self.owner, self.product_photo1.product_id + 10)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert product_photos_before == product_photos_after


@pytest.mark.django_db
class TestCreateProductPhotoService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product = ProductTestHelper.create_product(self.owner)
        self.create_product_photo_dict = {
            "product_id": product.product_id,
            "image_url": "test_url",
            "is_main_photo": True,
        }
        self.service = CreateProductPhotoService()


    def test_create(self):
        product_photos_before = ProductPhoto.objects.all().count()
        result = self.service.create(self.token, self.owner, self.create_product_photo_dict)
        product_photos_after = ProductPhoto.objects.all().count()

        assert result == "Product photo created successfully."
        assert product_photos_before == product_photos_after - 1


    def test_create_invalid_product_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        self.create_product_photo_dict["product_id"] += 10
        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.owner, self.create_product_photo_dict)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert product_photos_before == product_photos_after


    def test_create_product_does_not_belong_to_the_user(self):
        product_photos_before = ProductPhoto.objects.all().count()
        user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        AuthenticationHelper.register_and_login_user(user2_data)
        user2 = User.objects.get(username=user2_data["username"])
        product = ProductTestHelper.create_product(user2)
        self.create_product_photo_dict = {
            "product_id": product.product_id,
            "image_url": "test_url",
            "is_main_photo": True,
        }

        with pytest.raises(InvalidInputData) as e:
            self.service.create(self.token, self.owner, self.create_product_photo_dict)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product with this id does not belong to the user." in str(e.value)
        assert product_photos_before == product_photos_after


@pytest.mark.django_db
class TestDeleteProductPhotoService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.product = ProductTestHelper.create_product(self.owner)
        self.product_photo = ProductPhotoTestHelper.create_product_photo(self.product, "path")
        self.product_photo_id = self.product_photo.product_photo_id
        self.service = DeleteProductPhotoService()


    def test_delete(self):
        product_photos_before = ProductPhoto.objects.all().count()
        result = self.service.delete(self.token, self.owner, self.product_photo_id)
        product_photos_after = ProductPhoto.objects.all().count()

        assert result == "Product photo deleted successfully."
        assert product_photos_before == product_photos_after + 1


    def test_delete_invalid_product_photo_id(self):
        product_photos_before = ProductPhoto.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, self.owner, self.product_photo_id + 10)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product photo with this id does not exist." in str(e.value)
        assert product_photos_before == product_photos_after


    def test_delete_product_does_not_belong_to_the_user(self):
        product_photos_before = ProductPhoto.objects.all().count()
        user2_data = {"email": "test2@example.com", "username": "tester2", "password": "Abc123#ab",
                           "is_verified": True, "bio": "I'm new here!", "money": 0.00, "is_superuser": False,
                           "last_login": None, "address": "fweffwe", "postal_code": "00001", "city": "Warsaw",
                           "country": "Poland"}
        AuthenticationHelper.register_and_login_user(user2_data)
        user2 = User.objects.get(username=user2_data["username"])

        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, user2, self.product_photo_id)
        product_photos_after = ProductPhoto.objects.all().count()

        assert f"Product photo with this id does not belong to the user." in str(e.value)
        assert product_photos_before == product_photos_after
