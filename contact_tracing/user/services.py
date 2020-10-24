
from .models import User
from .models import ContactsRel
from .selectors import *


def create_user(
    *,
    mac: str
) -> User:
    user = User(mac=mac, status='gei').save()
    
    return user


def mark_positive(user: User):
    user1 = get_user(mac = user.mac)

    user1.status = "Positive"
    user1.safety = 0

    user1.save()
