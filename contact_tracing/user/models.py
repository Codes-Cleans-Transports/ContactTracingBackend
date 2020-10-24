from django.db import models
from neomodel import StructuredNode, StructuredRel, Relationship
from neomodel import UniqueIdProperty, DateTimeProperty, IntegerProperty, StringProperty, FloatProperty
from neomodel import cardinality

# Create your models here.
class ContactsRel(StructuredRel):
    start =  DateTimeProperty(required=True)
    duration = IntegerProperty(required=True)

class User(StructuredNode):
    mac = StringProperty(unique_index=True, required=True)
    safety = FloatProperty(default=1)
    status = StringProperty(required=True)

    contacts = Relationship(
        'User', 
        'CONTACTS',
        model=ContactsRel,
        cardinality=cardinality.ZeroOrMore,
    )

