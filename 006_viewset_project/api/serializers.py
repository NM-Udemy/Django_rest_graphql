from rest_framework import serializers
from .models import Facility, Equipment, FacilityType, UserPicture
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id', 'name', 'detail')
        read_only_fields = ('id',)

class EquipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'quantity', 'facility')
        read_only_fields = ('id',)


class FacilityTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FacilityType
        fields = ('id', 'name', 'facility')
        read_only_fields = ('id',)

class UserRegistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password',)
    
    def save(self):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('認証に失敗しました')
 
class UserPictureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPicture
        fields = ('image',)
 
 
class UserProfileSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    
    def save(self, **kwargs):
        user = self.context['user']
        user.username = self.validated_data.get('username', user.username)
        user.email = self.validated_data.get('email', user.email)
        user.first_name = self.validated_data.get('first_name', user.first_name)
        user.last_name = self.validated_data.get('last_name', user.last_name)
        user.save()
        return user