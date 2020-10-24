from datetime import datetime
from user.models import User, ContactsRel

def create_contact(
    *,
    mac1: str,
    mac2: str,
) -> ContactsRel:
    user1 = User.nodes.get(mac=mac1)
    user2 = User.nodes.get(mac=mac2)
    start = datetime.today().date()
    contact = user1.contacts.connect(user2,{'start':start, 'duration':1})

    return contact
