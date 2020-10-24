from django.db import models
from neomodel import *


# Create your models here.
class ContactsRel(StructuredRel):
    start =  DateTimeProperty(required=True)
    duration = IntegerProperty(required=True)

class User(StructuredNode):
    mac = StringProperty(unique_index=True, required=True)
    status = StringProperty(choices={"negative": "negative", "positive": "positive"}, default="negative")
    safety = FloatProperty(default=1)
    
    contacts = Relationship('User', 'CONTACTS', model=ContactsRel)


