from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Projects.as_view(), name="projects"),
    path('project/<str:pk>', views.SingleProject.as_view(), name="project"),
    path('create-project/', login_required(views.CreateProject.as_view(),
         login_url='login'), name="create-project"),
    path('update-project/<str:pk>',
         login_required(views.UpdateProject.as_view(), login_url='login'), name="update-project"),
    path('delete-project/<str:pk>',
         login_required(views.DeleteProject.as_view(), login_url='login'), name="delete-project"),
]
