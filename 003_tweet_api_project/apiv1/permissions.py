from rest_framework.permissions import BasePermission


class TweetUpdateDeletePermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return False
        elif request.method in ['PUT', 'DELETE']:
            return obj.user == request.user
        return True