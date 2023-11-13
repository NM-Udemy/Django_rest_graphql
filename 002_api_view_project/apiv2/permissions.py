from rest_framework.permissions import BasePermission, SAFE_METHODS
from . import views

class CustomPermission(BasePermission):
    
    def has_permission(self, request, view):
        # print(dir(request))
        # print(request.META['REMOTE_ADDR'])
        if request.user.is_authenticated:
            return True
        if isinstance(view, views.ItemModelDetailView):
            if request.method == 'DELETE':
                return False
            return True
        if request.META['REMOTE_ADDR'] == '127.0.0.1':
            return False
        if request.method == 'GET':
            return True
        # print(view)
        return False

class ProductPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return obj.user == request.user
        return True
