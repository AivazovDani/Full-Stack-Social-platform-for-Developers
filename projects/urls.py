from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.singleProject, name="project"),

    path('add-project/', views.createProject, name="add-project"),
    path('edit-project/<str:pk>/', views.editProject, name="edit-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project")
    ]

from django.contrib.auth import views as auth_views