import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import ToDo, Column
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id
from django.core.exceptions import ObjectDoesNotExist

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)
        fields = '__all__'

class ToDoNode(DjangoObjectType):
    class Meta:
        model = ToDo
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'priority': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
        fields = '__all__'

class OrderByEnum(graphene.Enum):
    TITLE_ASC = "title"
    TITLE_DESC = "-title"
    PRIORITY_ASC = "priority"
    PRIORITY_DESC = "-priority"

class ToDoQuery(graphene.ObjectType):
    todo = graphene.relay.Node.Field(ToDoNode)
    all_todos = DjangoFilterConnectionField(ToDoNode,
                                    orderBy=graphene.List(of_type=OrderByEnum))
    todo_by_global_id = graphene.Field(ToDoNode, global_id=graphene.ID(required=True))
    
    def resolve_all_todos(root, info, **kwargs):
        queryset = ToDo.objects.all()
        if "orderBy" in kwargs:
            order_by_fields = kwargs.get("orderBy")
            order_by_fields = [item.value for item in order_by_fields]
            # print(order_by_fields)
            queryset = queryset.order_by(*order_by_fields)
        return queryset
    
    def resolve_todo_by_global_id(root, info, global_id):
        try:
            _type, _id = from_global_id(global_id)
            print(_type, _id)
            return ToDo.objects.get(id=_id)
        except ObjectDoesNotExist:
            return None

class ColumnNode(DjangoObjectType):
    class Meta:
        model = Column
        interfaces = (graphene.relay.Node,)
        filter_fields = ['title',]
        fields = '__all__'

class ColumnQuery(graphene.ObjectType):
    column = graphene.relay.Node.Field(ColumnNode)
    all_columns = DjangoFilterConnectionField(ColumnNode)

class Query(graphene.ObjectType):
    todo_query = graphene.Field(ToDoQuery)
    column_query = graphene.Field(ColumnQuery)
    node = graphene.relay.Node.Field()
    
    def resolve_todo_query(root, info):
        return ToDoQuery()

    def resolve_column_query(root, info):
        return ColumnQuery()
