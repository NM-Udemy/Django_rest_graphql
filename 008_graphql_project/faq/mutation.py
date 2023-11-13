import graphene
from .query import QuestionType
from .models import Question, Category
from django.shortcuts import get_object_or_404

class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)
    
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.Int()
    
    @classmethod
    def mutate(cls, root, info, title, content, category_id):
        category = get_object_or_404(Category, pk=category_id)
        question = Question.objects.create(
            title = title,
            content = content,
            category = category,
        )
        return CreateQuestion(question=question)

class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)
    
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.Int()
    
    @classmethod
    def mutate(cls, root, info, id, title=None, content=None, category_id=None):
        question = get_object_or_404(Question, id=id)
        if title:
            question.title = title
        if content:
            question.content = content
        if category_id:
            category = get_object_or_404(Category, id=id)
            question.category = category
        question.save()
        return UpdateQuestion(question=question)

class DeleteQuestion(graphene.Mutation):
    is_deleted = graphene.Boolean()
    
    class Arguments:
        id = graphene.ID()
    
    @classmethod
    def mutate(cls, root, info, id):
        question = get_object_or_404(Question, id=id)
        if question:
            question.delete()
            return DeleteQuestion(is_deleted=True)
        return DeleteQuestion(is_deleted=False)

class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()
