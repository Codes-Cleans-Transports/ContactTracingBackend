from django.urls import path
from .views import ContactCreateDetailView
contact_patterns = [
    path('<mac>/', ContactCreateDetailView.as_view(), name='contact_create_detail'),
]