from django.urls import path, re_path
from authapp.views import login, logout, register_account, edit_account, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register_account, name='register'),
    path('edit/', edit_account, name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
