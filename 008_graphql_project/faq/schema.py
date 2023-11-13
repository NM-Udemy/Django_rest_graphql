import graphene
from .query import Query2, QuestionType, AnswerType
from .mutation import Mutation


schema = graphene.Schema(query=Query2, mutation=Mutation,
                         types=[QuestionType, AnswerType])
