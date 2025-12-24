from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUser, name='register-user'),
    path('login/', views.LoginUser, name='login-user'),

    path('logout/', views.LogoutUser, name='logout-user'),
]
