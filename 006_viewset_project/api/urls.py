from django.urls import path, include
from .views import (
    FacilityViewSet, EquipmentViewSet,
    FacilityTypeViewSet, UserViewSet,
    UserPictureViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('facility', FacilityViewSet, basename='facility')
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register('facility_type', FacilityTypeViewSet, basename='facility_type')
router.register('user', UserViewSet, basename='user')
router.register('user', UserPictureViewSet, basename='user_picture')


urlpatterns = [
    path('', include(router.urls)),
]
