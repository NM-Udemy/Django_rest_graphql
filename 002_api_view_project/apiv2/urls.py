from django.urls import path
from . import views

app_name = 'apiv2'

urlpatterns = [
    path('item/', views.ItemModelView.as_view(), name='item_model'),
    path('item/<int:pk>/', views.ItemModelDetailView.as_view(), name='item_model_detail'),
    path('user/', views.UserModelView.as_view(), name='user_model'),
    path('user/<int:pk>/', views.UserModelDetailView.as_view(), name='user_model_detail'),
    path('product/', views.ProductModelView.as_view(), name='product_model'),
    path('product/<int:pk>/', views.ProductModelDetailView.as_view(), name='product_model_detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]