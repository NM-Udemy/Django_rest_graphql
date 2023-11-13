from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from tweet_api_project.models import Tweet


class UserRegistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(
            validated_data['username'], email=validated_data['email'],
            password=validated_data['password'],
        )

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username,
                                password=password)
            if not user:
                raise serializers.ValidationError('ログインできません')
        else:
            raise serializers.ValidationError('ユーザー名とパスワードを送ってください')
        data['user'] = user
        return data
    
class TweetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = ('pk', 'text', 'created_at')
        read_only_field = ('pk', 'created_at',)
    
    def create(self, validated_data):
        return Tweet.objects.create(
            text=validated_data.get('text'),
            user=self.context.get('user'),
        )