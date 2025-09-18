from store.helper_classes.serializer_id_checker import SerializerHelper


class CheckIdSerializer:
    def __init__(self, id: int, name: str):
        self._id = id
        self._error = None
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def error(self):
        return self._error

    @property
    def name(self):
        return self._name

    @error.setter
    def error(self, new_error):
        self._error = new_error

    def is_valid(self) -> bool:
        error_messages = {"empty": f"{self.name} id cannot be empty.",
                          "not_positive_int": f"{self.name} id must be positive integer."}
        self.error = SerializerHelper.return_id_error(self.id, error_messages)
        if self.error:
            return False
        return True
