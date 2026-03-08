from decimal import Decimal, InvalidOperation

from store.serializers.check_id_serializer import CheckIdSerializer
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
        return self._validate_total_price()

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
