from datetime import datetime
from user.models import User, ContactsRel
from user.services import process_get_or_create_user



def process_create_or_update_contacts(
    *,
    user,
    macs
) -> None:
    for mac in macs:
        target = process_get_or_create_user(mac=mac)
        create_or_update_contact(user1=user, user2=targer)

def create_or_update_contact(
    *,
    user1: User,
    user2: User
) -> ContactsRel:

    if user1.contacts.is_created(user2):
        relationship = user1.contacts.relationship(user2)
        relationship.duration += 1
        relationship.save()
    else:
        relationship = user1.contacts.connect(user2, {'duration': 1})
    
    return relationship
