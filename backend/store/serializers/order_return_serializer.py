from store.helper_classes.serializer_id_checker import SerializerHelper


class CreateOrderReturnSerializer:
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
        error_messages_product_id = {"empty": "Order product id cannot be empty.",
                                     "not_positive_int": "Order product id must be positive integer."}
        return self._validate_id("order_product_id", error_messages_product_id) and self._validate_description()

    def _validate_id(self, key: str, error_messages: dict) -> bool:
        error = SerializerHelper.return_id_error(self.data.get(key), error_messages)
        if error:
            self.errors[key] = error
            return False
        self.validated_data[key] = self.data[key]
        return True

    def _validate_description(self):
        description = self.data.get("description")
        if description is None:
            self.errors["description"] = "Description cannot be empty."
        elif not isinstance(description, str):
            self.errors["description"] = "Description must be string."
        elif len(description.strip()) > 1024:
            self.errors["description"] = "Description must be less than 1025 characters."
        else:
            self.validated_data["description"] = description.strip()
            return True
        return False
