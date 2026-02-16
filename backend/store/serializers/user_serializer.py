from decimal import Decimal, InvalidOperation


class UpdateUserSerializer:
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
        return self._validate_money() and self._validate_bio()

    def _validate_money(self) -> bool:
        raw_value = self.data.get("money")

        if raw_value is None:
            self._errors["money"] = "Money cannot be empty."
            return False
        if isinstance(raw_value, str):
            raw_value = raw_value.replace(",", ".")
        try:
            price = Decimal(str(raw_value))
        except InvalidOperation:
            self._errors["money"] = "Money must be a valid decimal number."
            return False

        if price < Decimal("0.01") or price > Decimal("999999.99"):
            self._errors["money"] = "Money must be between 0.01 and 999999.99."
            return False

        self._validated_data["money"] = price
        return True

    def _validate_bio(self) -> bool:
        bio = self.data.get("bio")
        if bio is None:
            self.validated_data["bio"] = ""
            return True
        elif not isinstance(bio, str):
            self.errors["bio"] = "Bio must be string."
        else:
            self.validated_data["bio"] = bio
            return True
        return False