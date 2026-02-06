class CreateProductPhotoSerializer:
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
        return self._validate_product_id() and self._validate_image_url() and self._validate_is_main_photo()

    def _validate_product_id(self):
        product_id = self.data["product_id"]
        if not product_id:
            self.errors["product_id"] = "Product id cannot be empty."
        elif not isinstance(product_id, int) or product_id < 1:
            self.errors["product_id"] = "Product id must be positive integer."
        else:
            self.validated_data["product_id"] = product_id
            return True
        return False

    def _validate_image_url(self):
        image_url = self.data["image_url"]
        if not image_url:
            self.errors["image_url"] = "Image url cannot be empty."
        elif not isinstance(image_url, str):
            self.errors["image_url"] = "Image url must be a string."
        elif len(image_url.strip()) > 2048:
            self.errors["image_url"] = "Image url cannot be longer than 2048 characters."
        else:
            self.validated_data["image_url"] = image_url.strip()
            return True
        return False

    def _validate_is_main_photo(self):
        is_main_photo = self.data["is_main_photo"]
        if is_main_photo is None:
            self.errors["is_main_photo"] = "Is main photo flag cannot be empty."
        elif not isinstance(is_main_photo, bool):
            self.errors["is_main_photo"] = "Is main photo flag must be bool."
        else:
            self.validated_data["is_main_photo"] = is_main_photo
            return True
        return False
