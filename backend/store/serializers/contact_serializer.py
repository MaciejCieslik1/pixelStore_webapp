class CreateContactSerializer:
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
        if not self.data["receiver_username"]:
            self.errors["receiver_username"] = "Username cannot be empty."
        elif not isinstance(self.data["receiver_username"], str):
            self.errors["receiver_username"] = "Username must be a string."
        elif len(self.data["receiver_username"].strip()) > 32:
            self.errors["receiver_username"] = "Username cannot be longer than 32 characters."
        else:
            self.validated_data["receiver_username"] = self.data["receiver_username"].strip()
            return True
        return False
