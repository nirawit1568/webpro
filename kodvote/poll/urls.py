from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add_poll/', views.add_poll, name='add_poll'),
    path('my_poll/', views.my_poll, name='my_poll'),
    path('save_poll/', views.save_poll, name='save_poll'),
    path('view_detail/<int:poll_id>/', views.view_detail, name='view_detail'),
    path('poll_vote/<int:poll_id>/', views.poll_vote, name='poll_vote'),
    path('edit_poll/<int:poll_id>/', views.edit_poll, name='edit_poll')
]