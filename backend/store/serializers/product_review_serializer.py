from store.helper_classes.serializer_id_checker import SerializerHelper
from store.serializers.check_id_serializer import CheckIdSerializer
from store.serializers.check_username_serializer import CheckUsernameSerializer


class FindAllProductReviewsSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return self._validate_page() and self._validate_page_size()

    def _validate_page(self):
        page = self.data.get("page", 1)
        if page or page == 0:
            try:
                page = int(page)
                if page < 1:
                    raise ValueError
                self.validated_data["page"] = page
            except ValueError:
                self.errors["page"] = "Page number must be a positive integer."
                return False
            return True
        self.validated_data["page"] = 1
        return True

    def _validate_page_size(self):
        page_size = self.data.get("page_size", 10)
        if page_size or page_size == 0:
            try:
                page_size = int(page_size)
                if page_size < 1 or page_size > 100:
                    raise ValueError
                self.validated_data["page_size"] = page_size
            except ValueError:
                self.errors["page_size"] = "Page size must be between 1 and 100."
                return False
            return True
        self.validated_data["page_size"] = 10
        return True


class FindAllFromUserProductReviewsSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return self._validate_page() and self._validate_page_size()

    def _validate_page(self):
        page = self.data.get("page", 1)
        if page or page == 0:
            try:
                page = int(page)
                if page < 1:
                    raise ValueError
                self.validated_data["page"] = page
            except ValueError:
                self.errors["page"] = "Page number must be a positive integer."
                return False
            return True
        self.validated_data["page"] = 1
        return True

    def _validate_page_size(self):
        page_size = self.data.get("page_size", 10)
        if page_size or page_size == 0:
            try:
                page_size = int(page_size)
                if page_size < 1 or page_size > 100:
                    raise ValueError
                self.validated_data["page_size"] = page_size
            except ValueError:
                self.errors["page_size"] = "Page size must be between 1 and 100."
                return False
            return True
        self.validated_data["page_size"] = 10
        return True


class CreateProductReviewSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = {}
        self._errors = {}

    @property
    def data(self):
        return self._data

    @property
    def validated_data(self):
        return self._validated_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return self._validate_product_id() and self._validate_rating() and self._validate_description()

    def _validate_product_id(self) -> bool:
        product_id = self.data.get("product_id")
        id_serializer = CheckIdSerializer(product_id, "Product")
        if id_serializer.is_valid():
            self.validated_data["product_id"] = product_id
            return True
        self.errors["product_id"] = id_serializer.error
        return False

    def _validate_rating(self) -> bool:
        rating = self.data.get("rating")
        if rating is None:
            self.errors["rating"] = "Rating cannot be empty."
        elif not (isinstance(rating, float) or isinstance(rating, int)) or rating < 1 or rating > 5:
            self.errors["rating"] = "Rating must be decimal value from 1 to 5."
        else:
            self.validated_data["rating"] = rating
            return True
        return False

    def _validate_description(self) -> bool:
        description = self.data.get("description")
        if description is None:
            self.errors["description"] = "Description cannot be empty."
        elif not isinstance(description, str):
            self.errors["description"] = "Description must be text."
        elif len(description) > 1024 or len(description) < 1:
            self.errors["description"] = "Description length must be between 1 and 1024 characters."
        else:
            self.validated_data["description"] = description.strip()
            return True
        return False
