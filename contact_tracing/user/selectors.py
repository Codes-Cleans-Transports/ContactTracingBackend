from .models import User
from neomodel import db

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

    query = f"MATCH (n:User) WHERE n.mac='{mac}' MATCH (n)-[r:CONTACTS*0..{range}]-(m) RETURN DISTINCT m.mac, m.safety;"
    return db.cypher_query(query)[0]


def get_user_conections():
    query = f"MATCH (n)-[:CONTACTS*1..1]-(m) RETURN n.mac, m.mac"
    return db.cypher_query(query)



