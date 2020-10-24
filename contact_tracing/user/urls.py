from django.urls import path
from .views import UserDetailsView


user_patterns = [
    path('<mac>', UserDetailsView.as_view(), name='user_details')
]