import pytest

from store.exceptions import InvalidInputData
from store.helper_tests_classes.authentication_test_helper import AuthenticationHelper
from store.helper_tests_classes.product_test_helper import ProductTestHelper
from store.models import User, Product
from store.service.product_service import FindByIdProductService, FindAllProductsService, CreateProductService, \
    UpdateProductService, DeleteProductService


@pytest.mark.django_db
class TestFindProductByIdService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.product = ProductTestHelper.create_product(self.owner)
        self.service = FindByIdProductService()
        self.product_id = self.product.product_id
        self.product_dict = {
            "product_id": self.product_id,
            "owner_username": self.product.owner.username,
            "name": self.product.name,
            "description": self.product.description,
            "price": "1000.00",
            "amount": self.product.amount,
            "color": self.product.color,
            "weight": "0.45",
            "length": "15.00",
            "width": "15.00",
            "height": "0.80",
            "guarantee_period": self.product.guarantee_period,
            "status": self.product.status
        }

    def test_find_by_id(self):
        products_before = Product.objects.all().count()
        result = self.service.find_by_id(self.token, self.owner, self.product_id)
        products_after = Product.objects.all().count()

        assert result == self.product_dict
        assert products_before == products_after

    def test_find_by_id_invalid_id(self):
        products_before = Product.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_by_id(self.token, self.owner, self.product_id + 1)
        products_after = Product.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert products_before == products_after


@pytest.mark.django_db
class TestFindAllProductsService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        product1 = Product(owner=self.owner, name="aaa", description="example", price=100, amount=10, color="black",
                          weight=0.45, length=15.0, width=15.0, height=0.8, guarantee_period=24, status="AVAILABLE")
        product1.save()
        product2 = Product(owner=self.owner, name="bbb", description="example", price=150, amount=10, color="black",
                           weight=0.45, length=15.0, width=15.0, height=0.8, guarantee_period=24, status="AVAILABLE")
        product2.save()
        product3 = Product(owner=self.owner, name="ccc", description="example", price=200, amount=10, color="black",
                           weight=0.45, length=15.0, width=15.0, height=0.8, guarantee_period=24, status="UNAVAILABLE")
        product3.save()
        self.service = FindAllProductsService()
        self.product1_dict = {"product_id": product1.product_id, "owner_username": product1.owner.username, "name": product1.name,
            "description": product1.description, "price": "100.00", "amount": product1.amount, "color": product1.color,
            "weight": "0.45", "length": "15.00", "width": "15.00", "height": "0.80",
            "guarantee_period": product1.guarantee_period, "status": product1.status}
        self.product2_dict = {"product_id": product2.product_id, "owner_username": product2.owner.username, "name": product2.name,
            "description": product2.description, "price": "150.00", "amount": product2.amount, "color": product2.color,
            "weight": "0.45", "length": "15.00", "width": "15.00", "height": "0.80",
            "guarantee_period": product2.guarantee_period, "status": product2.status}
        self.product3_dict = {"product_id": product3.product_id, "owner_username": product3.owner.username, "name": product3.name,
            "description": product3.description, "price": "200.00", "amount": product3.amount, "color": product3.color,
            "weight": "0.45", "length": "15.00", "width": "15.00", "height": "0.80",
            "guarantee_period": product3.guarantee_period, "status": product3.status}
        self.data = {"owner_username": self.owner.username, "name": None, "min_price": None, "max_price": None, "status": None,
            "ordering_field": None, "order": None, "page": None, "page_size": None}

    def test_find_all_no_filters(self):
        product_dicts = [self.product1_dict, self.product2_dict, self.product3_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_owner_username(self):
        self.data["owner_username"] = self.user_data["username"]
        self.data["ordering_field"] = "name"
        product_dicts = [self.product1_dict, self.product2_dict, self.product3_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_name(self):
        self.data["name"] = "bbb"
        product_dicts = [self.product2_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_min_max_price(self):
        self.data["min_price"] = 100
        self.data["max_price"] = 150
        self.data["ordering_field"] = "name"
        product_dicts = [self.product1_dict, self.product2_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_min_max_price_desc(self):
        self.data["min_price"] = 100
        self.data["max_price"] = 150
        self.data["ordering_field"] = "name"
        self.data["order"] = "desc"
        product_dicts = [self.product2_dict, self.product1_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_min_max_price_no_match(self):
        self.data["min_price"] = 250
        self.data["max_price"] = 300
        product_dicts = []
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_status(self):
        self.data["status"] = "available"
        product_dicts = [self.product1_dict, self.product2_dict]
        products_before = Product.objects.all().count()
        result = self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert result == product_dicts
        assert products_before == products_after

    def test_find_all_filter_bad_owner_username(self):
        self.data["owner_username"] = self.user_data["username"] + "drfe"
        self.data["ordering_field"] = "name"

        products_before = Product.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.find_all(self.token, self.owner, self.data)
        products_after = Product.objects.all().count()

        assert "Product from seller with provided username does not exist." in str(e.value)
        assert products_before == products_after


@pytest.mark.django_db
class TestCreateProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.service = CreateProductService()
        self.product_dict = {"owner_username": self.owner.username, "name": "aaa",
            "description": "bbb", "price": 100, "amount": 1, "color": "red",
            "weight": 2, "length": 2, "width": 2, "height": 2,
            "guarantee_period": 24, "status": "available"}
        self.creation_communicate = "Product created successfully."

    def test_create(self):
        products_before = Product.objects.all().count()

        result = self.service.create(self.token, self.owner, self.product_dict)
        products_after = Product.objects.all().count()

        assert result == self.creation_communicate
        assert products_before == products_after - 1


@pytest.mark.django_db
class TestUpdateProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.product = ProductTestHelper.create_product(self.owner)
        self.service = UpdateProductService()
        self.product_id = self.product.product_id
        self.update_communicate = "Product updated successfully."

    def test_update_available(self):
        products_before = Product.objects.all().count()

        result = self.service.update(self.token, self.owner, self.product_id)
        product = Product.objects.get(product_id=self.product_id)
        products_after = Product.objects.all().count()

        assert product.status == "unavailable"
        assert result == self.update_communicate
        assert products_before == products_after

    def test_update_unavailable(self):
        self.product.status = "unavailable"
        self.product.save()
        products_before = Product.objects.all().count()

        result = self.service.update(self.token, self.owner, self.product_id)
        product = Product.objects.get(product_id=self.product_id)
        products_after = Product.objects.all().count()

        assert product.status == "archived"
        assert result == self.update_communicate
        assert products_before == products_after

    def test_update_invalid_id(self):
        products_before = Product.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.update(self.token, self.owner, self.product_id + 1)
        products_after = Product.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert products_before == products_after


@pytest.mark.django_db
class TestDeleteProductService:
    def setup_method(self):
        self.user_data = AuthenticationHelper.return_exemplary_user_data()
        self.token = AuthenticationHelper.register_and_login_user(self.user_data)
        self.owner = User.objects.get(username=self.user_data["username"])
        self.product = ProductTestHelper.create_product(self.owner)
        self.service = DeleteProductService()
        self.product_id = self.product.product_id
        self.delete_communicate = "Product deleted successfully."

    def test_delete(self):
        products_before = Product.objects.all().count()

        result = self.service.delete(self.token, self.owner, self.product_id)
        products_after = Product.objects.all().count()

        assert result == self.delete_communicate
        assert products_before == products_after + 1


    def test_delete_invalid_id(self):
        products_before = Product.objects.all().count()
        with pytest.raises(InvalidInputData) as e:
            self.service.delete(self.token, self.owner, self.product_id + 1)
        products_after = Product.objects.all().count()

        assert f"Product with this id does not exist." in str(e.value)
        assert products_before == products_after
