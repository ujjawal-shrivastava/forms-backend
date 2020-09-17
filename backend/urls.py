from django.contrib import admin
from django.urls import path
from ariadne.contrib.django.views import GraphQLView, MiddlewareManager
from apps.auth_jwt.middleware import JSONWebTokenMiddleware

from apps.api.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema, middleware=(MiddlewareManager(JSONWebTokenMiddleware()))), name='graphql'),
]
