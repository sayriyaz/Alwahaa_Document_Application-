from django.urls import path
from core import views  # Make sure this import statement is correct

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients_list, name='clients_list'),
    path('documents/', views.documents_list, name='documents_list'),
    path('documents/add/', views.add_document, name='add_document'),
    path('documents/edit/<int:document_id>/', views.edit_document, name='edit_document'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('services/', views.services_list, name='services_list'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/dashboard/', views.task_dashboard, name='task_dashboard')
]
