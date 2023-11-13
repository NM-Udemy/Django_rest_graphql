import graphene
import random
import requests
from graphql import GraphQLError

class Address(graphene.ObjectType):
    city = graphene.String()
    is_primary_address = graphene.Boolean(default_value=True)
    latitude = graphene.Float(description="住所の緯度")
    longitude = graphene.Float(description="住所の経度")


class UserType(graphene.ObjectType):
    name = graphene.String(description="名前")
    age = graphene.Int(description="年齢")
    address = graphene.Field(Address)
    addresses = graphene.List(Address, name="address_list")
    
    
    def resolve_name(root, info):
        name_list = ["Alice", "Bob", "Charlie"]
        return random.choice(name_list)
    
    def resolve_age(root, info):
        return random.randint(20, 50)
    
    def resolve_address(root, info):
        user_address = {"city": "ExampleCity"}
        return Address(**user_address) # Address(city: ExampleCity)

    def resolve_addresses(root, info):
        user_addresses = [
            {"city": "ExampleCity1"},
            {"city": "ExampleCity2", "latitude": 145.5},
        ]
        return [
            Address(**user_address)
            for user_address in user_addresses
        ]

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    address = graphene.Field(Address)


class UserAPIType(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())
    user_list = graphene.List(User)
    
    def resolve_user(root, info, id):
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        
        # エラー処理
        response.raise_for_status()
        
        # jsonにする
        user = response.json()
        
        return User(
            id=user["id"],name=user["name"], email=user["email"],
            address=Address(
                city=user["address"]["city"],
                latitude=user["address"]["geo"]["lat"],
                longitude=user["address"]["geo"]["lng"],
            )
        )
    
    def resolve_user_list(root, info):
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        users = response.json()
        print(users)
        response_users = []
        for user in users:
            response_users.append(
                User(
            id=user["id"],name=user["name"], email=user["email"],
            address=Address(
                city=user["address"]["city"],
                latitude=user["address"]["geo"]["lat"],
                longitude=user["address"]["geo"]["lng"],
            )
        )
            )
        return response_users


# インタフェース
class MediaType(graphene.Interface):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)

class BookType(graphene.ObjectType):
    author = graphene.String()
    
    class Meta:
        interfaces = (MediaType,)

class MovieType(graphene.ObjectType):
    director = graphene.String()
    
    class Meta:
        interfaces = (MediaType,)

books = [
    BookType(id="b1", title="My book1", author="novelist A"),
    BookType(id="b2", title="My book2", author="novelist B"),
]

movies = [
    MovieType(id="m1", title="My Movie1", director="director A"),
    MovieType(id="m2", title="My Movie2", director="director B"),
]

class Query(graphene.ObjectType):
    user_query = graphene.Field(UserType)
    user_api_query = graphene.Field(UserAPIType)
    search_media = graphene.Field(MediaType,
                                  id=graphene.ID(required=True))
    search_media_list = graphene.List(MediaType)
    
    def resolve_user_query(parent, info):
        return UserType()
    
    def resolve_user_api_query(parent, info):
        return UserAPIType()
    
    def resolve_search_media(parent, info, id):
        for book in books:
            if book.id == id:
                return book
        for movie in movies:
            if movie.id == id:
                return movie
        return GraphQLError(f"id:{id}の対象が存在しません")
    
    def resolve_search_media_list(parent, info):
        return books + movies

schema = graphene.Schema(query=Query, types=[BookType, MovieType])
