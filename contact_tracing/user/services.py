
from .models import User
from .models import ContactsRel
from .selectors import *
from neomodel import DoesNotExist
from queue import Queue

class CustomTuple:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __eq__(self, obj):
        return isinstance(obj, CustomTuple) and obj.first == self.first and obj.second == self.second

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
            queue.put(CustomTuple(user, master_user))

def propagate_safety(master_user: User):
    queue = Queue()

	# Push all children onto the queue

    add_children(master_user, queue)
    import pdb;pdb.set_trace()
    
    while not queue.empty():
        # Remove the fist element of the queue
        custon_tuple = queue.get()
        user = custon_tuple.first
        master_user = custon_tuple.second
        vertex = user.contacts.all_relationships(master_user)[0]

        # Calculate the safety of child nodes
        newSafety = calculate_safety(user, vertex)
		
        if newSafety < user.safety :
            user.safety = newSafety
            user.save()
            add_children(user, queue)
