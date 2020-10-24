
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

    user1.status = "positive"
    user1.safety = 0

    user1.save()

def calc_occ_weight(occ: int) -> float:
    res = -1
    if occ <= 10:
	    res = 0.5 * occ
    elif occ <= 90:
	    res = 0.8823529411764706 * occ + 0.5882352941176521
    elif occ < 1000:
	    res = 0.020879120879120878 * occ + 78.12087912087912
    else:
	    res = 99

    return res / 100


def calculate_safety(incoming_user: User, vertex: ContactsRel) -> float:
    occurenses_weight = calc_occ_weight(vertex.duration)

    user_risk = 1 - incoming_user.safety

    result = occurenses_weight * user_risk
    return 1 - result
