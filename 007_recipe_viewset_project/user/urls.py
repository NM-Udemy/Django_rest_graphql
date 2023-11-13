from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserRegistViewSet, UserLoginViewSet

router = DefaultRouter()
router.register('', UserRegistViewSet, basename='user')
router.register('', UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]