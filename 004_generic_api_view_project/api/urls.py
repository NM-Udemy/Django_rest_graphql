from django.urls import path
from .views import PostAPIView, UserCreateAPIView, UserLoginAPIView, PostAPIDetailView, CommentListCreateAPIView, CommentRetrieveDestroyAPIView, PostFilterAPIView

app_name = 'api'

urlpatterns = [
    path('posts/', PostAPIView.as_view(), name='post_api_view'),
    path('posts/<title>/', PostFilterAPIView.as_view(), name='post_filter_api_view'),
    path('posts/<int:pk>/', PostAPIDetailView.as_view(), name='post_api_detail_view'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='comment_list_create_api_view'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentRetrieveDestroyAPIView.as_view(), name='comment_retrieve_destroy_api_view'),
    path('signup/', UserCreateAPIView.as_view(), name='user_create_api_view'),
    path('login/', UserLoginAPIView.as_view(), name='user_login_api_view'),
]