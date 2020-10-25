from django.db import models
from neomodel import *
import json


# Create your models here.
class ContactsRel(StructuredRel):
    durations = JSONProperty()

    def get_date_occurances(self, date):
        durations_dict = json.loads(self.durations)

        return durations_dict(str(date))

    def duration(self) -> int:
        occ_sum = 0

        for _, occurances in json.loads(self.durations).items():
            occ_sum += occurances
        
        return occ_sum

class User(StructuredNode):
    mac = StringProperty(unique_index=True, required=True)
    status = StringProperty(choices={"negative": "negative", "positive": "positive"}, default="negative")
    safety = FloatProperty(default=1)
    
    contacts = Relationship('User', 'CONTACTS', model=ContactsRel)


