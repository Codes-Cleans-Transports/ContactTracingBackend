from django.urls import path
from .views import ContactCreateView, ContactsDetailView

contact_patterns = [
    path('', ContactCreateView.as_view(), name='contact_create'),
    path('<mac>/', ContactsDetailView.as_view(), name='contact-detail'),
]