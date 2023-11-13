from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import login, authenticate
from . import serializers
from .permissions import TweetUpdateDeletePermission
from tweet_api_project.models import Tweet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
def login_cookie(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response('ログインできません', status=400)
    token, created = Token.objects.get_or_create(user=user)
    response = Response('ログインしました')
    response.set_cookie(key='auth_token', value=token.key, httponly=True)
    return response


class UserRegistView(APIView):
    serializer_class = serializers.UserRegistSerializer
    permission_classes = [permissions.AllowAny,]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

class UserLoginView(APIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = [permissions.AllowAny,]
    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            return Response('ログインしました', status=status.HTTP_202_ACCEPTED)
        return Response('リクエストが誤っています', status=status.HTTP_400_BAD_REQUEST)
        

class TweetListView(APIView):
    
    serializer_class = serializers.TweetSerializer
    
    def get(self, request):
        tweets = Tweet.objects.all().order_by('-created_at')
        serializer = self.serializer_class(tweets, many=True)
        response = Response(serializer.data)
        # response['Cache-Control'] = 'public, max-age=60'
        from django.utils.http import http_date
        from datetime import datetime, timedelta
        expires_datetime = datetime.now() + timedelta(minutes=1)
        response['Expires'] = http_date(expires_datetime.timestamp())
        return response
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={
            'user': request.user,
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("リクエストの内容に誤りがあります", status=status.HTTP_400_BAD_REQUEST)

class TweetUpdateDeleteView(APIView):
    
    serializer_class = serializers.TweetSerializer
    permission_classes = (TweetUpdateDeletePermission,)

    def get_object(self, request, pk):
        obj = Tweet.objects.get(pk=pk)
        self.check_object_permissions(request, obj)
        return obj
    
    def put(self, request, pk):
        tweet = self.get_object(request, pk)
        serializer = self.serializer_class(tweet, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        tweet = self.get_object(request, pk)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    