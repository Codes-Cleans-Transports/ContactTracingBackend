
from .models import User
from .models import ContactsRel


def create_user(
    *,
    mac: str
) -> User:
    user = User(mac=mac, status='gei').save()
    
    return user


def create_contact(
    *,
    mac1: str,
    mac2: str
) -> ContactsRel:
    user1 = User.nodes(mac=mac1)
    user2 = User.nodes(mac=mac2)

    contact = user1.contacts.connect(user2)

    import pdb;pdb.set_trace()

    return contact
