from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Companies
    path("companies/", views.companies_list, name="companies_list"),

    # Service Requests
    path("requests/", views.requests_list, name="requests_list"),

    # Tasks
    path("tasks/", views.tasks_list, name="tasks_list"),
    path("tasks/dashboard/", views.task_dashboard, name="task_dashboard"),

    # # Legacy
    # path("clients/", views.clients_list, name="clients_list"),
    # path("documents/", views.documents_list, name="documents_list"),
]
