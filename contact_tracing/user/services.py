
from .models import User
from .models import ContactsRel
from .selectors import *
from neomodel import DoesNotExist


def process_get_or_create_user(
    *,
    mac: str
) -> User:
    try:
        return User.nodes.get(mac=mac)
    except DoesNotExist:
        return create_user(mac=mac)


def create_user(
    *,
    mac: str
) -> User:
    user = User(mac=mac).save()
    
    return user


def mark_positive(user: User):
    user1 = get_user(mac = user.mac)

    user1.status = "Positive"
    user1.safety = 0

    user1.save()
