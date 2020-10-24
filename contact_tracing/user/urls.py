from django.urls import path
from .views import UserCreateView, UserDetailsView


user_patterns = [
    path('', UserCreateView.as_view(), name='user_create'),
    path('<mac>', UserDetailsView.as_view(), name='user_details')
]