from decimal import Decimal, InvalidOperation

from store.serializers.check_username_serializer import CheckUsernameSerializer


class CreateTransactionSerializer:
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
        return self._validate_buyer_username() and self._validate_total_price()

    def _validate_buyer_username(self) -> bool:
        username = self.data.get("buyer_username")
        username_serializer = CheckUsernameSerializer(username)
        if username_serializer.is_valid():
            self.validated_data["buyer_username"] = username
            return True
        self.errors["buyer_username"] = username_serializer.error
        return False

    def _validate_total_price(self) -> bool:
        raw_value = self.data.get("total_price")

        if raw_value is None:
            self._errors["total_price"] = "Total price cannot be empty."
            return False
        if isinstance(raw_value, str):
            raw_value = raw_value.replace(",", ".")
        try:
            price = Decimal(str(raw_value))
        except InvalidOperation:
            self._errors["total_price"] = "Total price must be a valid decimal number."
            return False

        if price < Decimal("0.01") or price > Decimal("999999.99"):
            self._errors["total_price"] = "Total price must be between 0.01 and 999999.99."
            return False

        self._validated_data["total_price"] = price
        return True


class UpdateTransactionSerializer:
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
        return self._validate_total_price() and self._validate_is_finished()


    def _validate_total_price(self) -> bool:
        raw_value = self.data.get("total_price")

        if raw_value is None:
            self._errors["total_price"] = "Total price cannot be empty."
            return False
        if isinstance(raw_value, str):
            raw_value = raw_value.replace(",", ".")
        try:
            price = Decimal(str(raw_value))
        except InvalidOperation:
            self._errors["total_price"] = "Total price must be a valid decimal number."
            return False

        if price < Decimal("0.01") or price > Decimal("999999.99"):
            self._errors["total_price"] = "Total price must be between 0.01 and 999999.99."
            return False

        self._validated_data["total_price"] = price
        return True

    def _validate_is_finished(self) -> bool:
        is_finished = self.data.get("is_finished")
        if is_finished is None:
            self.errors["is_finished"] = "Is finished field cannot be empty."
            return False
        elif not isinstance(is_finished, bool):
            self.errors["is_finished"] = "Is finished field must be boolean."
        else:
            self.validated_data["is_finished"] = is_finished
            return True
        return False
