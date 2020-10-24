from django.urls import path
from .views import UserDetailsPatchView


user_patterns = [
    path('<mac>', UserDetailsPatchView.as_view(), name='user_details_patch')
]