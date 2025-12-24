from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUser, name='register-user'),
    path('login/', views.LoginUser, name='login-user'),

    path('logout/', views.LogoutUser, name='logout-user'),

    path('forgot-password/', views.Forgot_Password_View, name='forgot-password'),
    path('reset-password-sent/<uuid:reset_id>/', views.Reset_Password_Sent_View, name='reset-password-sent'),
    path('reset-password/<uuid:reset_id>/', views.Reset_Password_View, name='reset-password')
]
