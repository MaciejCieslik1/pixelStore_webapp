from rest_framework.exceptions import ValidationError

class EmailAlreadyTakenError(ValidationError):
    pass

class UsernameAlreadyTakenError(ValidationError):
    pass

class MissingEmailError(ValidationError):
    pass

class MissingPasswordError(ValidationError):
    pass

class UserNotFoundError(ValidationError):
    pass

class InvalidPasswordError(ValidationError):
    pass
