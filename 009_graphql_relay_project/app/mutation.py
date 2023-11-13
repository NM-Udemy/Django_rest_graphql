from .models import Column
from .query import ColumnNode
import graphene
from django.shortcuts import get_object_or_404
from graphql_relay.node.node import from_global_id
from graphql import GraphQLError

class CreateColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
    
    column = graphene.Field(ColumnNode)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        user = info.context.user
        title = inputs.get('title')
        description = inputs.get('description')
        column = Column.objects.create(
            title=title, description=description, user=user
        )
        return CreateColumnMutation(column=column)


class UpdateColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
    
    column = graphene.Field(ColumnNode)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        id = inputs.get('id')
        title = inputs.get('title')
        description = inputs.get('description')
        model_type, model_id = from_global_id(id)
        column = get_object_or_404(Column, pk=model_id)
        if title is not None:
            column.title = title
        if description is not None:
            column.description = description
        column.save()
        return UpdateColumnMutation(column=column)

class DeleteColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    ok = graphene.Boolean()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        id = inputs.get('id')
        model_type, model_id = from_global_id(id)
        column = get_object_or_404(Column, pk=model_id)
        column.delete()
        return DeleteColumnMutation(ok=True)

class Mutation(graphene.ObjectType):
    create_column = CreateColumnMutation.Field()
    update_column = UpdateColumnMutation.Field()
    delete_column = DeleteColumnMutation.Field()
    