from rest_framework.exceptions import ValidationError


class EmailAlreadyTakenError(ValidationError):
    pass


class UsernameAlreadyTakenError(ValidationError):
    pass