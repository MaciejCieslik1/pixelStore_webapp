from store.helper_classes.authentication_helper import DataValidator


class FindCategoryByNameSerializer:
    def __init__(self, name: str):
        self._name = name
        self._validated_name = None
        self._error = None

    @property
    def name(self):
        return self._name

    @property
    def validated_name(self):
        return self._validated_name

    @property
    def error(self):
        return self._error

    @validated_name.setter
    def validated_name(self, new_validated_name):
        self._validated_name = new_validated_name

    @error.setter
    def error(self, new_error):
        self._error = new_error


    def is_valid(self) -> bool:
        min_length = 0
        max_length = 32
        name = self.name

        if name is None or not name.strip():
            self.error = "Category name is not provided."
            return False
        name = name.strip()
        if not DataValidator.validate_length(name, min_length, max_length):
            self.error = "Category name cannot be longer than 32 characters."
            return False

        self.validated_name = name
        return True


class CreateCategorySerializer:
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
        return self._validate_name() and self._validate_description()

    def _validate_name(self):
        min_length = 0
        max_length = 32
        name = self.data.get("name")

        if name is None or not name.strip():
            self.errors["name"] = "Category name is not provided."
            return False
        name = name.strip()
        if not DataValidator.validate_length(name, min_length, max_length):
            self.errors["name"] = "Category name cannot be longer than 32 characters."
            return False

        self.validated_data["name"] = name
        return True

    def _validate_description(self):
        min_length = 0
        max_length = 1024
        description = self.data.get("description")

        if description is None or not description.strip():
            self.errors["description"] = "Description is not provided."
            return False
        description = description.strip()
        if not DataValidator.validate_length(description, min_length, max_length):
            self.errors["description"] = "Description cannot be longer than 1024 characters."
            return False

        self.validated_data["description"] = description
        return True
