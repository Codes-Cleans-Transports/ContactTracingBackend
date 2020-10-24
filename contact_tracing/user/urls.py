from django.urls import path
from .views import UserCreateView


user_patterns = [
    path('', UserCreateView.as_view(), name='user_create')
]