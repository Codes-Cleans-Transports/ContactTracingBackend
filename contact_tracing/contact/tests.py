from django.test import TestCase

from user.models import User

from datetime import datetime

from neomodel import db

from contact.services import *

from contact.utils import gen_today_occurances
from random import randrange

# Create your tests here.

class ContactsTests(TestCase):

    def setUp(self):
        db.cypher_query("MATCH (n) DETACH DELETE n;")

    def test_create_or_update_contact(self):
        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        create_or_update_contact(user1 = user1, user2 = user2)

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 1)

    def test_update_contact(self):
        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        user1.contacts.connect(user2, {'durations': gen_today_occurances(90)})
        create_or_update_contact(user1 = user1, user2 = user2)

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 91)

        