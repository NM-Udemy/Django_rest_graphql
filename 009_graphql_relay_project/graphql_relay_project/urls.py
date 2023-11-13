
from django.contrib import admin
from django.urls import path
from app import schema
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .middlewares import JWTMiddleware


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True,)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
