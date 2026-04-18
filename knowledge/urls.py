from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('create/', views.article_create, name='create'),
    path('<int:pk>/', views.article_detail, name='detail'),
    path('<int:pk>/update/', views.article_update, name='update'),
    path('<int:pk>/delete/', views.article_delete, name='delete'),
]
