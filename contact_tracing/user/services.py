
from .models import User
from .models import ContactsRel
from .selectors import *
from neomodel import DoesNotExist
from queue import Queue

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
    user.status = "positive"
    user.safety = 0
    user.save()
    propagate_safety(user)


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


def add_children(master_user: User, queue: Queue):
    for user in master_user.contacts.all():
            queue.put((user, master_user))


def propagate_safety(master_user: User):
    queue = Queue()

	# Push all children onto the queue
    add_children(master_user, queue)

    while not queue.empty():
        # Remove the fist element of the queue
        user, master_user = queue.get()
        user = get_user(mac = user.mac)
        master_user = get_user(mac = master_user.mac)

        vertex = user.contacts.all_relationships(master_user)[0]
        
        # Calculate the safety of child nodes
        newSafety = calculate_safety(master_user, vertex)

        if newSafety < user.safety :
            user.safety = newSafety
            user.save()
            add_children(user, queue)


