from rest_framework import serializers
from .models import Movie, Role, Staff, Comment, MovieRating
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import models

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['name', 'birthday']

class RoleSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True)
    class Meta:
        model = Role
        fields = ['name', 'staffs']



class MovieSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    average_star = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'content', 'roles', 'average_star']
    
    
    def get_average_star(self, obj):
        rating = MovieRating.objects.filter(movie=obj).first()
        if rating:
            return rating.average_star
        return "レーティングがありません"
        
    #     return obj.comments.all().aggregate(models.Avg('star')).get('star__avg')

class RoleDetailSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True)
    movie = serializers.StringRelatedField()
    
    class Meta:
        model = Role
        fields = ['name', 'staffs', 'movie']


class StaffDetailSerializer(serializers.ModelSerializer):
    roles = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Staff
        fields = ['name', 'birthday', 'roles']


class UserRegistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError('認証できませんでした')
        else:
            raise serializers.ValidationError('ユーザー名とパスワードを入力してください')
        data['user'] = user
        return data

class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(many=False, read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'star', 'comment', 'movie', 'user']
    
    def validate_star(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('0~5の整数を入力してください')
        return value
    
    def check_comment_existance(self, user, movie_id):
        if Comment.objects.filter(user=user, movie_id=movie_id).exists():
            raise serializers.ValidationError('すでにコメントしています')
    