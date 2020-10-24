from django.test import TestCase

from user.models import User

from datetime import datetime

from neomodel import db

from user.services import *

# Create your tests here.

class ContactsTests(TestCase):

    def setUp(self):
        db.cypher_query("MATCH (n) DETACH DELETE n;")

    def test_connect(self):

        date = datetime.today()

        user1 = User(mac = "mac1", status = "Negative").save()
        user2 = User(mac = "mac2", status = "Negative").save()

        user1.contacts.connect(user2, {'start': date, 'duration': 1})

    def test_mark_positive(self):
        user1 = User(mac = "mac1", status = "Negative").save()

        mark_positive(user1)

        user1 = get_user(mac = user1.mac)
        self.assert_(user1.status == "Positive")
        self.assertAlmostEqual(user1.safety, 0)



