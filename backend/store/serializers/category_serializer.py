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

    def is_valid(self) -> bool:
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
        return True
