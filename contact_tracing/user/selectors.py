
from .models import User

def get_user(
    *,
    mac: str
) -> User:

    return User.nodes.get(mac=mac)

def get_users_risk(
    *,
    mac: str,
    range: int
) -> User:

    import pdb;pdb.set_trace()
    query = self.cypher(f"MATCH (n:User) WHERE n.mac='{mac}' MATCH (n)-[r:CONTACTS*0..{range}]-(m) RETURN m.mac, m.risk;")

    return query

