from ariadne import ObjectType
from django.contrib.auth import authenticate
from apps.auth_jwt.decorators import login_required
from apps.auth_jwt.exceptions import UserExistsError, InvalidPasswordError, UserDoesNotExistError, TokenExpiredError, TokenInvalidError
from django.contrib.auth import get_user_model
from .tasks import send_register_email, send_forgot_password_email
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from django.conf import settings
from decouple import config

user = ObjectType("User")

@login_required
def resolve_user(_,info):
    user = get_user_model().objects.prefetch_related('forms').get(email=info.context.user.email)
    if user and user.is_active:
        return user

@user.field("email")
def resolve_user_email(obj,*_):
    return obj.email

@user.field("name")
def resolve_user_name(obj,*_):
    return obj.name.title()

@user.field("forms")
def resolve_user_forms(obj,*_):
    return obj.forms.all()



def resolve_register(_,info,email,password,name):
    user = get_user_model().objects.filter(email=email).exists()
    if user:
        raise UserExistsError()
    else:
        user = get_user_model().objects.create_user(email=email,password=password,name=name)
        send_register_email.delay(user.email,password, user.name)
        return user


@login_required
def resolve_change_name(_,info,name):
    user = get_user_model().objects.get(email=info.context.user.email)
    if user and user.is_active:
        user.name = name
        user.save()
        return user

@login_required
def resolve_change_password(_,info,old, new):
    user = authenticate(email=info.context.user.email, password=old)
    if user is None:
        raise InvalidPasswordError(f"Wrong password for {info.context.user.email}!")
    else:
        user1 = authenticate(email=info.context.user.email, password=new)
        if user1 is not None:
            raise InvalidPasswordError("New password cannot be same as the older one!")
        else:
            user.set_password(new)
            user.save()
            return True


def resolve_logout(_,info):
    return True


def resolve_forgot_password_request(_,info,email):
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        raise UserDoesNotExistError(f"User with email {email} does not exist!")
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    send_forgot_password_email.delay(email=email,name=user.name, url=f"{config('DASHBOARD_URL',default='http://deform.ujjawal.co', cast=str)}/forgot/{s.dumps(email)}")
    return True

def resolve_forgot_password_check(_,info,token):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        s.loads(token,max_age=1800)
    except SignatureExpired:
        raise TokenExpiredError()
    except BadSignature:
        raise TokenInvalidError()

    return True

def resolve_forgot_password_reset(_,info,token,new):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email= s.loads(token,max_age=1800)
    except SignatureExpired:
        raise TokenExpiredError()
    except BadSignature:
        raise TokenInvalidError()
    
    user = get_user_model().objects.get(email=email)
    if user is None:
        raise UserDoesNotExistError(f"User {email} no longer exist on server!")
    else:
        user.set_password(new)
        user.save()
        return user