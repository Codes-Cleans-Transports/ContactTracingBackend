from django.test import TestCase

from user.models import User

from datetime import datetime

from neomodel import db

from user.services import *

from random import randrange

# Create your tests here.

class ContactsTests(TestCase):

    def setUp(self):
        db.cypher_query("MATCH (n) DETACH DELETE n;")

    def test_connect(self):
        date = datetime.today()

        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        user1.contacts.connect(user2, {'start': date, 'duration': 1})

    def test_mark_positive(self):
        date = datetime.today()

        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()

        user1.contacts.connect(user2, {'start': date, 'duration': 90})

        mark_positive(user1)

        user1 = get_user(mac = user1.mac)
        user2 = get_user(mac = user2.mac)
        self.assert_(user1.status == "positive")
        self.assertAlmostEqual(user1.safety, 0)
        self.assertAlmostEqual(user2.safety, 0.2)

    def test_calc_occ_weight(self):
        self.assertEqual(calc_occ_weight(0), 0)
        self.assertEqual(calc_occ_weight(10), 0.05)
        self.assertEqual(calc_occ_weight(90), 0.8)
        self.assertEqual(calc_occ_weight(999990), 0.99)
        
        res = calc_occ_weight(randrange(1, 10))
        self.assertTrue( 0 < res and res < 0.05)

        res = calc_occ_weight(randrange(11, 89))
        self.assertTrue( 0.05 < res and res < 0.8)

        res = calc_occ_weight(randrange(90, 999))
        self.assertTrue( 0.8 < res and res < 1)

    def test_calculate_safety(self):
        occ = 10
        safety = 1
        vertex = ContactsRel(start=datetime.today(), duration = occ)
        user = User(mac="mac1", status = "negative", safety = safety)

        self.assertEqual(calculate_safety(user, vertex), 1.0)

        occ = 10
        safety = 0
        vertex = ContactsRel(start=datetime.today(), duration = occ)
        user = User(mac="mac1", status = "negative", safety = safety)

        self.assertEqual(calculate_safety(user, vertex), 0.95)

        occ = 90
        safety = .5
        vertex = ContactsRel(start=datetime.today(), duration = occ)
        user = User(mac="mac1", status = "negative", safety = safety)

        self.assertEqual(calculate_safety(user, vertex), 0.6)

    def test_add_children(self):
        date = datetime.today()

        user1 = User(mac = "mac1", status = "negative").save()
        user2 = User(mac = "mac2", status = "negative").save()
        user3 = User(mac = "mac3", status = "negative").save()

        user1.contacts.connect(user2, {'start': date, 'duration': 1})
        user1.contacts.connect(user3, {'start': date, 'duration': 1})

        queue = Queue()

        add_children(user1, queue)

        result = []
        while not queue.empty():
            result.append(queue.get())

        self.assertTrue((user2, user1) in result)
        self.assertTrue((user3, user1) in result)

    def test_propagate_safety_simple(self):
        date = datetime.today()

        user1 = User(mac = "mac1", status = "negative", safety = 0).save()
        user2 = User(mac = "mac2", status = "negative", safety = 1).save()
        user3 = User(mac = "mac3", status = "negative", safety = 1).save()

        user1.contacts.connect(user2, {'start': date, 'duration': 90})
        user1.contacts.connect(user3, {'start': date, 'duration': 10})

        propagate_safety(user1)

        user1 = get_user(mac = user1.mac)
        user2 = get_user(mac = user2.mac)
        user3 = get_user(mac = user3.mac)

        self.assertEqual(user1.safety, 0)
        self.assertAlmostEqual(user2.safety, 0.2)
        self.assertEqual(user3.safety, 0.95)
        

    def test_propagate_safety_loop(self):
        date = datetime.today()

        user1 = User(mac = "mac1", status = "negative", safety = 0).save()
        user2 = User(mac = "mac2", status = "negative", safety = 1).save()
        user3 = User(mac = "mac3", status = "negative", safety = 1).save()

        user1.contacts.connect(user2, {'start': date, 'duration': 90})
        user1.contacts.connect(user3, {'start': date, 'duration': 10})
        user2.contacts.connect(user3, {'start': date, 'duration': 50})

        propagate_safety(user1)

        user1 = get_user(mac = user1.mac)
        user2 = get_user(mac = user2.mac)
        user3 = get_user(mac = user3.mac)

        self.assertEqual(user1.safety, 0)
        self.assertAlmostEqual(user2.safety, 0.2)
        self.assertTrue(0.05 < user3.safety and user3.safety < 0.95)

        