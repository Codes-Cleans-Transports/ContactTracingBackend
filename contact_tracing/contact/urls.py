from django.urls import path
from .views import ContactCreateView

contact_patterns = [
    path('', ContactCreateView.as_view(), name='contact_create')
]