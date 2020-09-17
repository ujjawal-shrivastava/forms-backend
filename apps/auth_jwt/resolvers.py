"""ariadne_django_jwt resolvers module"""
from ariadne import gql
from django.contrib.auth import authenticate, get_user_model
from .exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    MaximumTokenLifeReachedError,
    InvalidPasswordError,
    UserDoesNotExistError
)
from .utils import create_jwt, decode_jwt, refresh_jwt, create_long_jwt


auth_token_definition = gql(
    """
    type AuthToken {
        token: String
        email: String
        name:String
        verified:Boolean
        long: Boolean
    }
"""
)

auth_token_verification_definition = gql(
    """
    type AuthTokenVerification {
        valid: Boolean!
        user: String
    }
"""
)


def resolve_token_auth(parent, info,long=False, **credentials):
    """Resolves the token auth mutation"""
    token = None
    email= None
    name = None
    user = authenticate(info.context, **credentials)

    if user is not None:
        email=user.email
        name=user.name
        verified = user.verified
        if long:
            token = create_long_jwt(user)
        else:
            token = create_jwt(user)

    
    if user is None:
        try:
            user = get_user_model().objects.get(email=credentials["email"])
        except get_user_model().DoesNotExist:
            raise UserDoesNotExistError(f" User '{credentials['email']}' does not exist!")
        if user is not None:
            raise InvalidPasswordError(f"Wrong password for {credentials['email']}!")

    return {"token": token, "long":long, "email":email, "name":name, "verified":verified}


def resolve_refresh_token(parent, info, token):
    """Resolves the resfresh token mutaiton"""

    try:
        token = refresh_jwt(token)

    except (InvalidTokenError, MaximumTokenLifeReachedError):
        token = None

    return {"token": token}


def resolve_verify_token(parent, info, token: str):
    """Resolves the verify token mutation"""
    token_verification = {}

    try:
        decoded = decode_jwt(token)
        token_verification["valid"] = True
        token_verification["user"] = decoded.get("user")

    except (InvalidTokenError, ExpiredTokenError):
        token_verification["valid"] = False

    return token_verification
