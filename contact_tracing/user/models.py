from django.db import models
from neomodel import StructuredNode, StructuredRel, RelationshipTo
from neomodel import UniqueIdProperty, DateProperty, IntegerProperty, StringProperty

# Create your models here.
class ContactsRel(StructuredRel):
    start =  DateProperty(required=True)
    duration = IntegerProperty(required=True)

class User(StructuredNode):
    mac = StringProperty(unique_index=True, required=True)
    status = StringProperty(required=True)

    contacts = RelationshipTo('User', 'CONTACTS', model=ContactsRel) # cardinality is zero or more

