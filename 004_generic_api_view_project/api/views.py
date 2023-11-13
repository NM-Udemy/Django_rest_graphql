from django.shortcuts import render
from .models import Post, Comment
from .serializers import PostSerializer, UserCreateSerializer, UserLoginSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     ListCreateAPIView,
                                     GenericAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveDestroyAPIView
                                     )
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend


class CommentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
    def perform_update(self, serializer):
        comment = self.get_object()
        if(self.request.user.id != comment.author.id):
            raise PermissionError('ログインユーザーとコメント投稿者が異なります')
        serializer.save()

    def perform_destroy(self, instance):
        comment = self.get_object()
        if(self.request.user.id != comment.author.id):
            raise PermissionError('ログインユーザーとコメント投稿者が異なります')
        instance.delete()

class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments = Comment.objects.filter(post_id=post_id)
        return comments
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        user = self.request.user
        serializer.save(author=user, post_id = post_id)

class PostAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
# class PostListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 5
#     last_page_strings = ('l', )
# class PostListLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 3
#     max_limit = 7
#     limit_query_param = 'l'
#     offset_query_param = 'o'
class PostCursorPagination(CursorPagination):
    # page_size = 3
    # cursor_query_param = 'c'
    ordering = '-id'
    
class CustomFilterBackend(BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        title = request.query_params.get('title')
        title_sw = request.query_params.get('title_sw')
        title_ew = request.query_params.get('title_ew')
        order_by = request.query_params.get('order_by')
        filter_queryset = queryset
        if title:
            filter_queryset = filter_queryset.filter(title=title)
        if title_sw:
            filter_queryset = filter_queryset.filter(title__startswith=title_sw)
        if title_ew:
            filter_queryset = filter_queryset.filter(title__endswith=title_ew)
        if order_by:
            filter_queryset = filter_queryset.order_by(order_by)
        return filter_queryset
    
    
class PostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filter_backends = [CustomFilterBackend,]
    # filter_backends = [OrderingFilter,]
    # # ordering_fields = ['title', 'content']
    # ordering_fields = '__all__'
    # ordering = ['-title']
    
    # filter_backends = [SearchFilter,]
    # # ^ 前方一致、= 完全一致、@ 全文検索, $ 正規表現
    # search_fields = ['title', 'content', '$comments__comment']
    # filterset_class = PostFilter
    
    # filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ['title', 'author__username']
    # pagination_class = PostCursorPagination
    # pagination_class = PostListPagination
    # pagination_class = PostListLimitOffsetPagination
    
    def get_queryset(self):
        posts = Post.objects.prefetch_related('comments').all()
        return posts
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

   
class PostFilterAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    # pagination_class = PostCursorPagination
    # pagination_class = PostListPagination
    # pagination_class = PostListLimitOffsetPagination
    
    def get_queryset(self):
        title = self.kwargs.get('title')
        posts = Post.objects.filter(title=title)
        posts = posts.prefetch_related('comments').all()
        return posts
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserCreateAPIView(CreateAPIView):
    
    model = User
    serializer_class = UserCreateSerializer

class UserLoginAPIView(GenericAPIView):
    
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={
            'request': request,
        })
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data['username'])
            user = serializer.validated_data['user']
            login(request, user)
            return Response('ログインしました', status=status.HTTP_202_ACCEPTED)
        return Response('リクエストが誤っています', status=status.HTTP_400_BAD_REQUEST)