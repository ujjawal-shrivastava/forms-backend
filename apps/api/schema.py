from ariadne import QueryType,MutationType,load_schema_from_path, make_executable_schema
from apps.account import resolvers as a_resolver
from apps.form import resolvers as f_resolver
from apps.auth_jwt.decorators import login_required
from apps.auth_jwt.resolvers import (
  auth_token_definition,
  auth_token_verification_definition,
  resolve_token_auth,
  resolve_refresh_token,
  resolve_verify_token,
)

type_defs = load_schema_from_path('apps/api/schema.graphql')
account_defs = load_schema_from_path('apps/account/schema.graphql')
form_defs = load_schema_from_path('apps/form/schema.graphql')

@login_required
def resolve_hello(_,info):
    ip = info.context.META["REMOTE_ADDR"]
    return f"Hello {info.context.user.email} from ip: {ip}"

query = QueryType()
query.set_field("hello",resolve_hello)
query.set_field("user",a_resolver.resolve_user)
query.set_field("forms",f_resolver.resolve_forms)
query.set_field("form",f_resolver.resolve_public_form)
query.set_field("getForm",f_resolver.resolve_get_form)
query.set_field("forgotPasswordVerify",a_resolver.resolve_forgot_password_check)
query.set_field("responses",f_resolver.resolve_responses)

mutation = MutationType()

#AUTH MUTATIONS
mutation.set_field("register",a_resolver.resolve_register)
mutation.set_field("login",resolve_token_auth)
mutation.set_field("logout",a_resolver.resolve_logout)
#mutation.set_field("refreshToken",resolve_token_auth)
#mutation.set_field("verifyToken",resolve_verify_token)
mutation.set_field("changeName",a_resolver.resolve_change_name)
mutation.set_field("changePassword",a_resolver.resolve_change_password)
mutation.set_field("forgotPassword",a_resolver.resolve_forgot_password_request)
mutation.set_field("forgotPasswordReset",a_resolver.resolve_forgot_password_reset)

#FORM MUTATIONS
mutation.set_field("saveForm",f_resolver.resolve_save_form)
mutation.set_field("deleteForm",f_resolver.resolve_delete_form)
mutation.set_field("publishForm",f_resolver.resolve_publish_form)
mutation.set_field("unpublishForm",f_resolver.resolve_unpublish_form)

#RESPONSE MUTATIONS
mutation.set_field("addResponse",f_resolver.resolve_add_response)

schema = make_executable_schema([type_defs,auth_token_definition, auth_token_verification_definition, account_defs, form_defs], [query,mutation, a_resolver.user, f_resolver.form, f_resolver.public_form])