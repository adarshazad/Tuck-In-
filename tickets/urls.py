from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list, name='list'),
    path('create/', views.ticket_create, name='create'),
    path('<int:pk>/', views.ticket_detail, name='detail'),
    path('<int:pk>/update/', views.ticket_update, name='update'),
    path('<int:pk>/delete/', views.ticket_delete, name='delete'),
    path('<int:pk>/close/', views.ticket_close, name='close'),
    path('<int:pk>/resolve/', views.ticket_resolve, name='resolve'),
]
