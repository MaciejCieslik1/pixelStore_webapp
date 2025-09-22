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

    @validated_username.setter
    def validated_username(self, new_validated_username):
        self._validated_username = new_validated_username

    def is_valid(self) -> bool:
        if not self.username:
            self.error = "Username cannot be empty."
        elif not isinstance(self.username, str):
            self.error = "Username must be a string."
        elif len(self.username.strip()) > 32:
            self.error = "Username cannot be longer than 32 characters."
        else:
            self.validated_username = self.username.strip()
            return True
        return False
