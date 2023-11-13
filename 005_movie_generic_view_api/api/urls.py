from django.urls import path
from .views import (
    MovieListCreate, MovieRetrieve, RoleRetrieve,
    StaffRetrieve, RegistUser, LoginUser, CommentListCreate,
    CommentRetrieveUpdateDestroy,)

app_name = 'api'

urlpatterns = [
    path('regist', RegistUser.as_view(), name='regist'),
    path('login', LoginUser.as_view(), name='login'),
    path('movies', MovieListCreate.as_view(), name='movie_list_create'),
    path('movies/<int:pk>', MovieRetrieve.as_view(), name='movie_retrieve'),
    path('roles/<int:pk>', RoleRetrieve.as_view(), name='role_retrieve'),
    path('staffs/<int:pk>', StaffRetrieve.as_view(), name='staff_retrieve'),
    path('movies/<int:movie_id>/comments', CommentListCreate.as_view(), name='comment_list_create'),
    path('movies/<int:movie_id>/comments/<int:pk>', CommentRetrieveUpdateDestroy.as_view(), name='comment_retrieve_update_destroy'),
]