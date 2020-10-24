
from .models import User
from .models import ContactsRel
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
