import jwt
from jwt import InvalidTokenError
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

class IncorrectTokenError(InvalidTokenError):
    pass

class TokenExpiredByReplacementError(InvalidTokenError):
    pass

class RefreshTokenExpiredError(jwt.ExpiredSignatureError):
    pass

class InvalidRefreshTokenError(jwt.InvalidTokenError):
    pass

class TokenTypeMismatchError(ValueError):
    pass

class CategoryNameAlreadyOccupiedError(ValueError):
    pass

class CategoryNotFoundError(ValueError):
    pass

class NotificationNotFoundError(ValueError):
    pass

class NotificationNotBelongToUserError(ValueError):
    pass

class InvalidUsernameError(ValueError):
    pass

class SelfUsernameError(ValueError):
    pass

class InvalidNotificationIdError(ValueError):
    pass

class NotificationIdDoesNotBelongToUserError(ValueError):
    pass

class InvalidInputData(ValueError):
    pass

class NotEnoughFundsError(ValueError):
    pass

class InvalidIdError(ValueError):
    pass
