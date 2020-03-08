from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_login, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('add_user/', views.add_user, name='add_user'),
]