# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest


class TestParty(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Party")

    def test_party(self):
        email_id = create_party()

        self.assertTrue(frappe.db.exists({"doctype": "Party", "email_id": email_id}))


def create_party():
    doc = frappe.new_doc("Party")
    doc.party_type = "Customer"
    doc.party_name = "Test Party"
    doc.email_id = "test_party@example.com"
    doc.mobile_number = None
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.email_id
