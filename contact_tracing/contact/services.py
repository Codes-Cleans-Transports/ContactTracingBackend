from datetime import datetime
from user.models import User, ContactsRel
from user.services import process_get_or_create_user

from user.services import propagate_safety

import json


def process_create_or_update_contacts(
    *,
    user,
    macs
) -> None:
    for mac in macs:
        target = process_get_or_create_user(mac=mac)
        create_or_update_contact(user1=user, user2=target)

def create_or_update_contact(
    *,
    user1: User,
    user2: User
) -> ContactsRel:

    if user1.contacts.is_connected(user2):
        relationship = user1.contacts.relationship(user2)
        durations = relationship.durations
        relationship.save()
    else:
        today = datetime.today().date()
        durations = {}
        durations[str(today)] = 1
        relationship = user1.contacts.connect(user2, {'durations': json.dumps(durations)})

    if user1.safety > user2.safety:
        propagate_safety(user2)
    else:
        propagate_safety(user1)
    
    return relationship
