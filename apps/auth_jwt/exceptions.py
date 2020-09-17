"""ariadne_django exceptions module"""

from django.utils.translation import ugettext_lazy as _


class JSONWebTokenError(Exception):
    """Generic JSON Web Token error"""

    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(JSONWebTokenError):
    default_message = _("You do not have permission to perform this action")


class LoginRequiredError(JSONWebTokenError):
    """Error for cases when a login is required to access the data"""

    default_message = _("Login is required")


class ExpiredTokenError(JSONWebTokenError):
    default_message = _("Signature has expired")


class MaximumTokenLifeReachedError(JSONWebTokenError):
    """Error for cases when refreshed tokens hit their maximum life limit"""

    default_message = _("The maximum life for this token has been reached")


class AuthenticatedUserRequiredError(JSONWebTokenError):
    """Error for cases when an authenticated user is required"""

    default_message = _("User is not authenticated")


class InvalidTokenError(JSONWebTokenError):
    """Error for cases when the provided JWT is not valid"""

    default_message = _("The provided string is not a valid JWT")


class UserExistsError(JSONWebTokenError):
    """Error for Registration when the user with email already exists """

    default_message = _("A user already exists with the provided email")

class InvalidPasswordError(JSONWebTokenError):
    """Error for cases when user exists but password is wrong"""

    default_message = _("Password is wrong")

class UserDoesNotExistError(JSONWebTokenError):
    """Error for cases when user does not exist"""

    default_message = _("User does not exist")

class TokenInvalidError(JSONWebTokenError):
    """Error for cases when password reset token is invalid"""

    default_message = _("Link is invalid or broken!")

class TokenExpiredError(JSONWebTokenError):
    """Error for cases when +password reset token is expired"""

    default_message = _("Link validity expired!")

class FormDoesNotExistError(JSONWebTokenError):
    """Error for cases when +password reset token is expired"""

    default_message = _("Form does not exist!")