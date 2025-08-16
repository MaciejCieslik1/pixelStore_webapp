import re

from store.helper_classes.authentication_helper import DataValidator


class RegisterSerializer:
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
        return (self._validate_username() and self._validate_email() and self._validate_password() and
            self._validate_address() and self._validate_postal_code() and self._validate_city() and
            self._validate_country())

    def _validate_username(self) -> bool:
        min_length = 3
        max_length = 16
        username = self.data.get("username")

        if username is None or not username.strip():
            self.errors["username"] = "Username is not provided."
            return False
        username = username.strip()
        if not DataValidator.validate_length(username, min_length, max_length):
            self.errors["username"] = f"Username must be between {min_length} and {max_length} characters."
            return False

        self.validated_data["username"] = username
        return True

    def _validate_email(self) -> bool:
        min_length = 0
        max_length = 64
        email = self.data.get("email")

        if email is None or not email.strip():
            self.errors["email"] = "Email is not provided."
            return False
        email = email.strip()
        if not DataValidator.validate_length(email, min_length, max_length):
            self.errors["email"] = "Email must have maximum 64 characters."
            return False

        self.validated_data["email"] = email
        return self._has_email_correct_parts(email)

    def _has_email_correct_parts(self, email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email) is None:
            self.errors["email"] = "Email is not valid."
            return False
        return True

    def _validate_password(self) -> bool:
        min_length = 8
        max_length = 64
        password = self.data.get("password")

        if password is None or not password.strip():
            self.errors["password"] = "Password is not provided."
            return False
        password = password.strip()
        if not DataValidator.validate_length(password, min_length, max_length):
            self.errors["password"] = f"Password must be between {min_length} and {max_length} characters."
            return False

        self.validated_data["password"] = password
        return self._has_password_essential_characters(password)

    def _has_password_essential_characters(self, password: str) -> bool:
        has_digit = re.search(r"\d", password)
        has_small_letter = re.search(r"[a-z]", password)
        has_capital_letter = re.search(r"[A-Z]", password)
        has_special_character = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if has_digit and has_small_letter and has_capital_letter and has_special_character:
            return True
        else:
            self.errors["password"] = "Password needs at least one small letter, \
                                                          capital letter, digit and special character."
            return False

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
        return self._has_place_only_letters(address, "address")

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



class LoginSerializer:
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
        return False


class AccountVerificationSerializer:
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
        return False


class TokenVerificationSerializer:
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
        return False


class RefreshTokenSerializer:
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
        return False


class ResetPasswordSerializer:
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
        return False


class ResendVerificationCodeSerializer:
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
        return False
