"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('spins/', views.UserSpinsView.as_view(), name='spins'),
    path('prizes/', views.UserPrizesView.as_view(), name='prizes'),
    path('reset_password/', views.ResetUserPasswordView.as_view(), name='reset_password'),
    path('reset_password/<str:uuid>/', views.ResetUserPasswordDeatilView.as_view(), name='reset_password_detail'),
]
