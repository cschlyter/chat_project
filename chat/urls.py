from django.urls import path

from . import views

urlpatterns = [
    path('users/register/', views.register, name='register'),
    path('users/login/', views.login_page, name='login'),
    path('users/logout/', views.logout_page, name='logout'),

    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
