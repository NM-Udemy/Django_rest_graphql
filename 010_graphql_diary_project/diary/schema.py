from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from graphene import relay
import graphene
from .models import Diary
from graphql_relay.node.node import from_global_id
from django.shortcuts import get_object_or_404

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")
        interfaces = (relay.Node,)

class CreateUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserType)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        username = inputs.get('username')
        password = inputs.get('password')
        user = User.objects.create_user(username=username, password=password)
        return CreateUser(user=user)

class DiaryType(DjangoObjectType):
    class Meta:
        model = Diary
        interfaces = (graphene.relay.Node,)
        fields = ("id", "title", "content", "created_at", "updated_at", "user")
        filter_fields = ['title',]

class Query(graphene.ObjectType):
    all_diaries = DjangoFilterConnectionField(DiaryType, orderBy=graphene.List(of_type=graphene.String))
    diary = graphene.relay.Node.Field(DiaryType)
    
    def resolve_all_diaries(root, info, **kwargs):
        queryset = Diary.objects.all()
        if "orderBy" in kwargs:
            order_by_fields = kwargs.get("orderBy")
            queryset = queryset.order_by(*order_by_fields)
        return queryset


class CreateDiary(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
    
    diary = graphene.Field(DiaryType)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("ログインが必要です")
        diary = Diary(title=inputs.get('title'), content=inputs.get('content'),
                      user=user)
        diary.save()
        return CreateDiary(diary=diary)

class UpdateDiary(relay.ClientIDMutation):
    
    class Input:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()
    
    diary = graphene.Field(DiaryType)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        _, id = from_global_id(inputs.get('id'))
        user = info.context.user
        if user.is_anonymous:
            raise Exception("ログインが必要です")
        diary = get_object_or_404(Diary, pk=id, user=user)
        if inputs.get('title') is not None:
            diary.title = inputs.get('title')
        if inputs.get('content') is not None:
            diary.content = inputs.get('content')
        diary.save()
        return UpdateDiary(diary=diary)


class DeleteDiary(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        _, id = from_global_id(inputs.get('id'))
        user = info.context.user
        if user.is_anonymous:
            raise Exception("ログインが必要です")
        diary = get_object_or_404(Diary, pk=id, user=user)
        diary.delete()
        return DeleteDiary(success=True)


class Mutation(graphene.ObjectType):
    create_diary = CreateDiary.Field()
    update_diary = UpdateDiary.Field()
    delete_diary = DeleteDiary.Field()
    create_user = CreateUser.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)