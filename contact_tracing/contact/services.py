from user.models import User, ContactsRel

def create_contact(
    *,
    mac1: str,
    mac2: str
) -> ContactsRel:
    user1 = User.nodes.get(mac=mac1)
    user2 = User.nodes.get(mac=mac2)

    contact = user1.contacts.connect(user2)

    import pdb;pdb.set_trace()

    return contact
