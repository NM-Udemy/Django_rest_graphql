from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserRegistSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    age = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = '__all__'
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise seiralizers.ValidationError('パスワードが一致しません')
        return data
    
    def save(self):
        user = CustomUser.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            age = self.validated_data['age'],
            password = self.validated_data['password']
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('認証に失敗しました')