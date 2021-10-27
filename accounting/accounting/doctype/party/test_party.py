# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import string
import random
import unittest


class TestParty(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        frappe.db.delete("Party")
        print("Party -> Passed")

    def test_create_party(self):
        frappe.set_user("Administrator")
        doc = frappe.new_doc("Party")
        doc.party_type = "Customer"
        doc.party_name = "Test Party"
        doc.email_id = "test_party" + "".join(random.choices(string.ascii_uppercase +
                                                             string.digits, k=5)) + "@example.com"
        doc.mobile_number = None
        doc.flags.ignore_mandatory = True
        doc.insert()
        party_name = frappe.db.get_value(
            "Party", doc.email_id, "party_name")

        self.assertEqual(party_name, doc.party_name)
