from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views

app_name = 'apiv1'

urlpatterns = [
    path('tweets/', views.TweetListView.as_view(), name='tweets'),
    path('tweets/<int:pk>',
         views.TweetUpdateDeleteView.as_view(), name='tweets_update_delete'),
    path('user/regist', views.UserRegistView.as_view(), name='user_regist'),
    path('api-token-auth', auth_views.obtain_auth_token),
    path('login_cookie', views.login_cookie, name='login_cookie'),
    # path('user/login', views.UserLoginView.as_view(), name='user_login'),
]