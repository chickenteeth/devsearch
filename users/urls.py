from re import L
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('', views.AllProfiles.as_view(), name="profiles"),
    path('profile/<str:pk>', views.UserProfile.as_view(), name="user-profile"),
    path('account/', login_required(views.UserAccount.as_view(),
         login_url='login'), name="account"),
    path('edit-account/', login_required(views.EditAccount.as_view(),
         login_url='login'), name='edit-account'),
    path('create-skill/', login_required(views.CreateSkill.as_view(),
         login_url='login'), name='create-skill'),
    path('update-skill/<str:pk>/', login_required(views.UpdateSkill.as_view(),
         login_url='login'), name='update-skill'),
    path('delete-skill/<str:pk>/', login_required(views.DeleteSkill.as_view(),
         login_url='login'), name='delete-skill'),
    path('inbox/', login_required(views.Inbox.as_view(),
         login_url='login'), name='inbox'),
    path('message/<str:pk>', login_required(views.ViewMessage.as_view(),
         login_url='login'), name='message'),
    path('create-message/<str:pk>/',
         views.CreateMessage.as_view(), name='create-message'),
]
