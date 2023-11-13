from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (ItemModelSerializer, UserModelSerializer,
ProductModelSerializer, LoginSerializer)
from rest_framework import status
from rest_framework import permissions
from .permissions import CustomPermission, ProductPermission
from api.models import Item, Product
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import TokenAuthentication

class BaseListView(APIView):
    
    def get(self, request):
        objects = self.model.objects.all()
        serializer = self.serializer_class(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # 保存(create) or 更新
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class BaseDetailView(APIView):
    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)
    
    def get_object(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        self.check_object_permissions(request, obj)
        return obj
    
    def put(self, request, pk):
        obj = self.get_object(request, pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        obj = self.get_object(request, pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    

class ItemModelView(BaseListView):
    serializer_class = ItemModelSerializer
    model = Item
    permission_classes = [CustomPermission,]

class ProductModelView(BaseListView):
    serializer_class = ProductModelSerializer
    model = Product
    authentication_classes = [TokenAuthentication,]
    
class UserModelView(BaseListView):
    serializer_class = UserModelSerializer
    model = get_user_model()

class ItemModelDetailView(BaseDetailView):
    
    serializer_class = ItemModelSerializer
    model = Item
    permission_classes = [CustomPermission,]


class ProductModelDetailView(BaseDetailView):
    
    serializer_class = ProductModelSerializer
    model = Product
    permission_classes = [ProductPermission,]



class UserModelDetailView(BaseDetailView):
    
    serializer_class = UserModelSerializer
    model = get_user_model()

class LoginView(APIView):
    
    permission_classes = [permissions.AllowAny,]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=self.request.data, 
                                     context={'request': self.request}
                                     )
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    
    permission_classes = [permissions.IsAuthenticated,]
    
    def post(self, request):
        logout(request)
        return Response('ログアウトしました', status=status.HTTP_202_ACCEPTED)
