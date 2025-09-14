class FindByIdOrderProductSerializer:
    def __init__(self, order_product_id: int):
        self._id = order_product_id
        self._error = None

    @property
    def id(self):
        return self._id

    @property
    def error(self):
        return self._error

    def is_valid(self) -> bool:
        return True


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
        return True


class UpdateOrderProductSerializer:
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


class DeleteOrderProductSerializer:
    def __init__(self, order_product_id: int):
        self._id = order_product_id
        self._error = None

    @property
    def id(self):
        return self._id

    @property
    def error(self):
        return self._error

    def is_valid(self) -> bool:
        return True
