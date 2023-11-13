from django.shortcuts import render
from .models import Movie, Role, Staff, Comment
from .serializers import (
    MovieSerializer, RoleDetailSerializer, StaffDetailSerializer,
    UserRegistSerializer, UserLoginSerializer, CommentSerializer,)
from rest_framework import generics, permissions, status
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class RegistUser(generics.CreateAPIView):
    serializer_class = UserRegistSerializer
    permission_classes = [permissions.AllowAny,]
    
    
class LoginUser(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny,]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context = {
            'request': request,
        })
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request,user)
            return Response('ログインしました', status=status.HTTP_202_ACCEPTED)
        return Response('リクエストに誤りがあります', status=status.HTTP_400_BAD_REQUEST)
            
class MovieListPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10

class MovieListCreate(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = MovieListPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'roles__staffs__name', 'year']
    ordering_fields = ['name', 'year']
    
    def get_queryset(self):
        return Movie.objects.filter(is_accepted=True)
    
class MovieRetrieve(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RoleRetrieve(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleDetailSerializer


class StaffRetrieve(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffDetailSerializer


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Comment.objects.filter(movie_id=movie_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        movie_id = self.kwargs.get('movie_id')
        serializer.check_comment_existance(user, movie_id)
        serializer.save(user=user, movie_id=movie_id)

class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
