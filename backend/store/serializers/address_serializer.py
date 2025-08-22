from store.helper_classes.authentication_helper import DataValidator


class UpdateAddressSerializer:
    def __init__(self, data: dict):
        self._data = data
        self._validated_data = data
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
        return self._validate_address() and self._validate_postal_code() and self._validate_city() and self._validate_country()

    def _validate_address(self) -> bool:
        min_length = 0
        max_length = 64
        address = self.data.get("address")

        if address is None or not address.strip():
            self.errors["address"] = "Address is not provided."
            return False
        address = address.strip()
        if not DataValidator.validate_length(address, min_length, max_length):
            self.errors["address"] = "Address cannot be longer than 64 characters."
            return False

        self.validated_data["address"] = address
        return True

    def _has_place_only_letters(self, place: str, place_category: str) -> bool:
        if place.isalpha():
            return True
        self.errors[place_category] = f"{place_category.capitalize()} should contain only letters."
        return False

    def _validate_postal_code(self) -> bool:
        postal_code = self.data.get("postal_code")

        if postal_code is None or not postal_code.strip():
            self.errors["postal_code"] = "Postal code is not provided."
            return False
        postal_code = postal_code.strip()
        if not len(postal_code) == 5:
            self.errors["postal_code"] = "Postal code must have exactly 5 digits."
            return False

        self.validated_data["postal_code"] = postal_code
        return self._has_postal_code_only_digits(postal_code)

    def _has_postal_code_only_digits(self, postal_code: str) -> bool:
        if postal_code.isdigit():
            return True
        self.errors["postal_code"] = "Postal must consist of exactly 5 digits."
        return False

    def _validate_city(self) -> bool:
        min_length = 0
        max_length = 64
        city = self.data.get("city")

        if city is None or not city.strip():
            self.errors["city"] = "City is not provided."
            return False
        city = city.strip()
        if not DataValidator.validate_length(city, min_length, max_length):
            self.errors["city"] = "City cannot be longer than 64 characters."
            return False

        self.validated_data["city"] = city
        return self._has_place_only_letters(city, "city")

    def _validate_country(self) -> bool:
        min_length = 0
        max_length = 64
        country = self.data.get("country")

        if country is None or not country.strip():
            self.errors["country"] = "Country is not provided."
            return False
        country = country.strip()
        if not DataValidator.validate_length(country, min_length, max_length):
            self.errors["country"] = "Country cannot be longer than 64 characters."
            return False

        self.validated_data["country"] = country
        return self._has_place_only_letters(country, "country")
