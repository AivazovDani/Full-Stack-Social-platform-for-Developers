from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('project/<str:pk>/vote', views.vote),
    path('remote-tag', views.removeTag)
]