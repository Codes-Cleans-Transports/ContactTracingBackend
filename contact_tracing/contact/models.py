from django.db import models
from neomodel import StructuredNode, StructuredRel, RelationshipTo
from neomodel import UniqueIdProperty, DateProperty, IntegerProperty, StringProperty

# Create your models here.
class User(StructuredNode):
    id = UniqueIdProperty()
    mac = StringProperty(unique_index=True, required=True)
    status = StringProperty(required=True)

    contacts = RelationshipTo('User', 'CONTACTS') # cardinality is zero or more

class ContactsRel(StructuredRel):
    start =  DateProperty(required=True)
    duration = IntegerProperty(required=True)