from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Facility, Equipment, FacilityType, UserPicture
from .serializers import (FacilitySerializer, EquipmentSerializer,
                          FacilityTypeSerializer, UserRegistSerializer,
                          UserLoginSerializer, UserProfileSerializer,
                          UserPictureSerializer)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import login

class FacilityViewSet(viewsets.ViewSet):
    # lookup_field = 'name'
    
    def list(self, request):
        queryset = Facility.objects.all()
        serializer = FacilitySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Facility.objects.all()
        facility = get_object_or_404(queryset, pk=pk)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = FacilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @action(detail=False, methods=['get'])
    def filter_list(self, request):
        name = request.query_params.get('name', None)
        if name is not None:
            queryset = Facility.objects.filter(name__contains=name)
            serializer = FacilitySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'no record'})
    
    @action(detail=True, methods=['get'])
    def custom_action(self, request, pk=None):
        return Response({'detail': 'custom_action'})
    

class EquipmentPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 10


class EquipmentViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = EquipmentPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'facility__name')
    
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FacilityTypeViewSet(viewsets.ModelViewSet):
    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    model = FacilityType

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserRegistSerializer
    permission_classes = (permissions.AllowAny,)
    
    @action(detail=False, methods=['post'])
    def regist(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            login(request, user)
            return Response(serializer.data, status=200)
        return Response(seiralizer.errors, status=400)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @profile.mapping.patch
    def patch_profile(self, request):
        serializer = UserProfileSerializer(context={'user': request.user},
                                           data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserPictureViewSet(viewsets.GenericViewSet):
    
    serializer_class = UserPictureSerializer
    
    def get_queryset(self):
        return UserPicture.objects.filter(user=self.request.user).all()
    
    @action(detail=False, methods=['post'])
    def upload_picture(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @upload_picture.mapping.get
    def get_uploaded_picture(self, reqeust):
        userPictures = self.get_queryset()
        serializers = self.serializer_class(userPictures, many=True)
        return Response(serializers.data, status=200)
    