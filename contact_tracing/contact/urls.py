from django.urls import path
from .views import ContactCreateView, ContactDetailView

contact_patterns = [
    path('', ContactCreateView.as_view(), name='contact_create'),
    path('<mac>/', ContactDetailView.as_view(), name='contact-detail'),
]