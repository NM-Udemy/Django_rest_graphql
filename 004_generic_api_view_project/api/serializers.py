from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.urls import reverse



class UserCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password,
                                )
            if not user:
                raise serializers.ValidationError('ログインできませんでした')
        else:
            raise serializers.ValidationError('入力が誤ってます')
        
        data['user'] = user
        return data

class CommentSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'comment', 'created_at', 'detail_url')
        read_only_fields = ('id','post', 'author', 'created_at')

    def get_detail_url(self, obj):
        return reverse('api:comment_retrieve_destroy_api_view', kwargs={'post_id': obj.post.id, 'pk': obj.pk})

class PostSerializer(serializers.ModelSerializer):
    
    comments = CommentSerializer(many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'comments', 'detail_url')
        read_only_fields = ('author', )

    def get_detail_url(self, obj):
        return reverse('api:post_api_detail_view', kwargs={'pk': obj.pk})