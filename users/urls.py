from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('', views.Profiles.as_view(), name="profiles"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
    path('inbox/', login_required(views.Inbox.as_view(),
         login_url='login'), name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='message'),
    path('create-message/<str:pk>/', views.createMessage, name='create-message'),
]
