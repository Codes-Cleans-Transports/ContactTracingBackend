
from .models import User
from .models import ContactsRel


def create_user(
    *,
    mac: str
) -> User:
    user = User(mac=mac, status='gei').save()
    
    return user


