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

class UserNotVerifiedError(ValidationError):
    pass

class NoVerificationCodeFoundError(ValidationError):
    pass

class InvalidVerificationCodeError(ValidationError):
    pass

class ExpiredVerificationCodeError(ValidationError):
    pass

class MissingCredentialsError(ValidationError):
    pass

class PasswordsNotMatchError(ValueError):
    pass

class TokenExpiredError(ValidationError):
    pass

class CannotGetTokenFromRequestError(ValueError):
    pass
