class UpdateUserPreferencesSerializer:
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
        return self._validate_dark_mode()

    def _validate_dark_mode(self) -> bool:
        dark_mode = self.data["dark_mode"]
        if dark_mode is None:
            self.validated_data["dark_mode"] = False
            return True
        elif not isinstance(dark_mode, bool):
            self.errors["dark_mode"] = "Dark mode must be bool."
        else:
            self.validated_data["dark_mode"] = dark_mode
            return True
        return False
