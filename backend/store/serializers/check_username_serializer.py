class CheckUsernameSerializer:
    def __init__(self, username: str):
        self._username = username
        self._validated_username = None
        self._error = None

    @property
    def username(self):
        return self._username

    @property
    def validated_username(self):
        return self._validated_username

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, new_error):
        self._error = new_error

    def is_valid(self) -> bool:
        return True
