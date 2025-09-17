from store.helper_classes.serializer_id_checker import SerializerHelper


class CreateOrderProductSerializer:
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
        error_messages_product_id = {"empty": "Product id cannot be empty.",
                          "not_positive_int": "Product id must be positive integer."}
        error_messages_transaction_id = {"empty": "Transaction id cannot be empty.",
                                     "not_positive_int": "Transaction id must be positive integer."}
        return (self._validate_id("product_id", error_messages_product_id) and
            self._validate_id("transaction_id", error_messages_transaction_id) and
            self._validate_seller_username() and self._validate_shopping_price())

    def _validate_id(self, key: str, error_messages: dict) -> bool:
        error = SerializerHelper.return_id_error(self.data.get(key), error_messages)
        if error:
            self.errors[key] = error
            return False
        self.validated_data[key] = self.data[key]
        return True

    def _validate_seller_username(self) -> bool:
        username = self.data.get("seller_username")
        if not isinstance(username, str) and username is not None:
            self.errors["seller_username"] = "Seller username must be string."
            return False
        if username is None or not username.strip():
            self.errors["seller_username"] = "Seller username cannot be empty."
            return False
        username = username.strip()
        self.validated_data["seller_username"] = username
        return True

    def _validate_shopping_price(self) -> bool:
        price = self.data.get("shopping_price")
        error = SerializerHelper.return_price_error(price)
        if error:
            self.errors["shopping_price"] = error
            return False
        self.validated_data["shopping_price"] = price
        return True

    def _validate_price(self):
        price = self.data.get("shopping_price")
        error = SerializerHelper.return_price_error(price)
        if error:
            self.errors["shopping_price"] = error
            return False
        self.validated_data["shopping_price"] = self.data["shopping_price"]
        return True
