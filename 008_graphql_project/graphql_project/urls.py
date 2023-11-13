from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from faq import schema
from user import schema as user_schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema.schema)),
    path('graphql_user', GraphQLView.as_view(graphiql=True, schema=user_schema.schema))
]
