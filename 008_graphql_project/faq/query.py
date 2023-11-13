import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Question, Answer
from graphql import GraphQLError

class CategoryType(DjangoObjectType):
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description',)


class QAInterface(graphene.Interface):
    id = graphene.ID()
    content = graphene.String()

class QuestionType(DjangoObjectType):
    
    class Meta:
        model = Question
        fields = '__all__'
        interfaces = (QAInterface,)
        
    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_published=True)


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        exclude = ('created_at',)
        interfaces = (QAInterface,)


class SearchUnion(graphene.Union):
    class Meta:
        types = (CategoryType, QuestionType)


class Query(graphene.ObjectType):
    all_questions = DjangoListField(QuestionType)
    all_categories = DjangoListField(CategoryType)
    all_answers = graphene.List(AnswerType, id=graphene.Int(), content=graphene.String())
    question = graphene.Field(QuestionType, id=graphene.Int())
    categories_filtered_by_name = graphene.List(
        CategoryType, name=graphene.String()
    )
    search_results = graphene.List(SearchUnion, term=graphene.String())
    search_result = graphene.Field(SearchUnion, term=graphene.String())
    
    def resolve_search_result(root, info, term):
        category = Category.objects.filter(name__contains=term).first()
        if category:
            return category
        question = Question.objects.filter(title__contains=term).first()
        return question
    
    def resolve_search_results(root, info, term=""):
        if term:
            categories = Category.objects.filter(name__contains=term)
            questions = Question.objects.filter(title__contains=term)
        else:
            categories = Category.objects.all()
            questions = Question.objects.all()
        return list(categories) + list(questions)

    def resolve_categories_filtered_by_name(root, info, name):
        return Category.objects.filter(name__contains=name)
    
    def resolve_question(root, info, id):
        return Question.objects.get(id=id)
    
    def resolve_all_answers(root, info, id=0, content=""):
        # id = kwargs.get('id')
        # content = kwargs.get('content')
        filters = {}
        if id:
            filters['id'] = id
        if content:
            filters['content__contains'] = content
        
        if filters:
            return Answer.objects.filter(**filters)
        return Answer.objects.all()

class Query2(graphene.ObjectType):
    question_query = graphene.Field(Query)
    search_qa = graphene.Field(QAInterface, q=graphene.String())
    search_qa_list = graphene.List(QAInterface, q=graphene.String())
    
    def resolve_question_query(parent, info):
        return Query()

    def resolve_search_qa(parent, info, q):
        question = Question.objects.filter(content__contains=q).first()
        if question:
            return question
        answer = Answer.objects.filter(content__contains=q).first()
        if answer:
            return answer
        return GraphQLError(f"{q}に対応する対象が見つかりませんでした")

    def resolve_search_qa_list(parent, info, q):
        questions = list(Question.objects.filter(content__contains=q))
        answers = list(Answer.objects.filter(content__contains=q))
        combined_list = questions + answers
        if combined_list:
            return combined_list
        return GraphQLError(f"{q}に対応する対象が見つかりませんでした")
        