from .serializers import UserRegistSerializer, UserLoginSerializer
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import login
from rest_framework.authtoken.models import Token


class UserRegistViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistSerializer
    permission_classes = (permissions.AllowAny,)
    
    @action(detail=False, methods=['post'])
    def regist(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors,status=400)
    
class UserLoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # login(request, serializer.validated_data)
            token = Token.objects.get_or_create(user=serializer.validated_data)
            return Response({"token": token[0].key}, status=200)
        return Response(serializer.errors, status=400)
