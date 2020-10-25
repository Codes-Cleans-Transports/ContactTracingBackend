from django.test import TestCase

from user.models import User

from datetime import datetime

from neomodel import db

from contact.services import *

from contact.utils import gen_occurances
from random import randrange

from datetime import datetime, timedelta

from user.selectors import get_user

from user.services import mark_positive

# Create your tests here.

class ContactsTests(TestCase):

    def setUp(self):
        db.cypher_query("MATCH (n) DETACH DELETE n;")

    def test_create_or_update_contact_simple(self):
        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        create_or_update_contact(user1 = user1, user2 = user2)

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 1)

    def test_create_or_update_contact_multiple_days(self):
        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        yesterday = datetime.today() - timedelta(days=1)
        user1.contacts.connect(user2, {'durations': gen_occurances(10, yesterday)})
        create_or_update_contact(user1 = user1, user2 = user2)

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 11)
        self.assertEqual(user1.contacts.all_relationships(user2)[0].get_date_occurances(yesterday), 10)
        self.assertEqual(user1.contacts.all_relationships(user2)[0].get_date_occurances(), 1)

    def test_update_contact(self):
        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        user1.contacts.connect(user2, {'durations': gen_occurances(90)})
        create_or_update_contact(user1 = user1, user2 = user2)

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 91)

    def test_end_to_end(self):
        user1 = process_get_or_create_user(mac="mac1")
        macs = ["mac2", "mac3"]

        process_create_or_update_contacts(user = user1, macs = macs)

        user2 = get_user(mac = "mac2")
        user3 = get_user(mac = "mac3")

        self.assertTrue(user1.contacts.is_connected(user2))
        self.assertTrue(user1.contacts.is_connected(user3))
        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 1)
        self.assertEqual(user1.contacts.all_relationships(user3)[0].duration(), 1)

        process_create_or_update_contacts(user = user2, macs = ["mac1", "mac3"])

        self.assertTrue(user2.contacts.is_connected(user1))
        self.assertTrue(user2.contacts.is_connected(user3))
        self.assertEqual(user2.contacts.all_relationships(user1)[0].duration(), 2)
        self.assertEqual(user2.contacts.all_relationships(user3)[0].duration(), 1)

        for number in range(2, 90):
            process_create_or_update_contacts(user = user1, macs = ["mac2"])

        for number in range(1, 10):
            process_create_or_update_contacts(user = user1, macs = ["mac3"])

        self.assertEqual(user1.contacts.all_relationships(user2)[0].duration(), 90)
        self.assertEqual(user1.contacts.all_relationships(user3)[0].duration(), 10)

        user1 = get_user(mac = "mac1")
        user2 = get_user(mac = "mac2")
        user3 = get_user(mac = "mac3")

        self.assertEqual(user1.safety, 1)
        self.assertEqual(user2.safety, 1)
        self.assertEqual(user3.safety, 1)

        mark_positive(user1)

        user1 = get_user(mac = "mac1")
        user2 = get_user(mac = "mac2")
        user3 = get_user(mac = "mac3")

        self.assertEqual(user1.safety, 0)
        self.assertAlmostEqual(user2.safety, 0.2)
        self.assertEqual(user3.safety, 0.95)

        