
from .models import User

def get_user(
    *,
    mac: str
) -> User:

    return User.nodes.get(mac=mac)
