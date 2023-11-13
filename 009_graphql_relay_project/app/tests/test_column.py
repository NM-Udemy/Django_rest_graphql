from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth.models import User
from app.models import Column
import json

# 変数の定義
USERNAME1 = "testuser1"
USERNAME2 = "testuser2"
PASSWORD = "testpassword"

COLUMN_TITLE1 = "TITLE 1"
COLUMN_DESCRIPTION1 = "DESCRIPTION 1"
COLUMN_TITLE2 = "TITLE 2"
COLUMN_DESCRIPTION2 = "DESCRIPTION 2"
COLUMN_TITLE3 = "TITLE 3"
COLUMN_DESCRIPTION3 = "DESCRIPTION 3"
COLUMN_TITLE4 = "TITLE 4"
COLUMN_DESCRIPTION4 = "DESCRIPTION 4"
COLUMN_TITLE5 = "TITLE 5"
COLUMN_DESCRIPTION5 = "DESCRIPTION 5"


class ColumnTestCase(GraphQLTestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username=USERNAME1, password=PASSWORD)
        cls.user2 = User.objects.create_user(username=USERNAME2, password=PASSWORD)
        
        cls.column1 = Column.objects.create(title=COLUMN_TITLE1, description=COLUMN_DESCRIPTION1, user=cls.user1)
        cls.column2 = Column.objects.create(title=COLUMN_TITLE2, description=COLUMN_DESCRIPTION2, user=cls.user1)
        cls.column3 = Column.objects.create(title=COLUMN_TITLE3, description=COLUMN_DESCRIPTION3, user=cls.user2)
        cls.column4 = Column.objects.create(title=COLUMN_TITLE4, description=COLUMN_DESCRIPTION4, user=cls.user2)
    
    def test_column_query(self):
        response = self.query(
            '''
            query MyQuery{
                columnQuery{
                    allColumns{
                        edges{
                            node{
                                title
                                description
                                user{
                                    username
                                }
                            }
                        }
                    }
                }
            }
            '''
        )
        column_data = json.loads(response.content)['data']['columnQuery']['allColumns']['edges']
        
        # 単体テストのチェック
        self.assertEqual(len(column_data), 3)
        
        expected_columns = [
            (COLUMN_TITLE1, COLUMN_DESCRIPTION1, USERNAME1),
            (COLUMN_TITLE2, COLUMN_DESCRIPTION2, USERNAME1),
            (COLUMN_TITLE3, COLUMN_DESCRIPTION3, USERNAME2),
        ]
        
        for i, column in enumerate(column_data):
            node = column['node']
            self.assertEqual(node['title'], expected_columns[i][0])
            self.assertEqual(node['description'], expected_columns[i][1])
            self.assertEqual(node['user']['username'], expected_columns[i][2])
    
    def fetch_column_by_title(self, title):
        return self.query(
            '''
            query MyQuery($title: String!){
                columnQuery{
                    allColumns(title: $title){
                        edges{
                            node{
                                title
                                description
                                user{
                                    username
                                }
                            }
                        }
                    }
                }
            }
            ''',
            variables={'title': title}
        )
        
    def check_column(self, response, title, description, username):
        column_data = json.loads(response.content)['data']['columnQuery']['allColumns']['edges']
        
        self.assertEqual(len(column_data), 1)
        node = column_data[0]['node']
        self.assertEqual(node['title'], title)
        self.assertEqual(node['description'], description)
        self.assertEqual(node['user']['username'], username)
     
    def test_column_by_title(self):
        response = self.fetch_column_by_title(COLUMN_TITLE1)
        self.check_column(response, COLUMN_TITLE1, COLUMN_DESCRIPTION1, USERNAME1)
        
    def test_create_column_no_login(self):
        response = self.query(
            '''
            mutation MyMutation($title: String!, $description: String!){
                createColumn(input: {title: $title, description: $description}){
                    column{
                        title
                        description
                    }
                }
            }
            ''',
            variables={'title': COLUMN_TITLE5, 'description': COLUMN_DESCRIPTION5}
        )
        self.assertIn('errors', json.loads(response.content))

    
    def login(self, username, password):
        response = self.client.post('/api/token/', 
                                    {'username': username, 'password': password})
        return json.loads(response.content)['access']
    
    def test_create_column_login(self):
        jwt_token = self.login(USERNAME1, PASSWORD)
        response = self.query(
            '''
            mutation MyMutation($title: String!, $description: String!){
                createColumn(input: {title: $title, description: $description}){
                    column{
                        title
                        description
                    }
                }
            }
            ''',
            variables={'title': COLUMN_TITLE5, 'description': COLUMN_DESCRIPTION5},
            headers={'HTTP_AUTHORIZATION': f'Bearer {jwt_token}'}
        )
        response = self.fetch_column_by_title(COLUMN_TITLE5)
        self.check_column(response, COLUMN_TITLE5, COLUMN_DESCRIPTION5, USERNAME1)
    