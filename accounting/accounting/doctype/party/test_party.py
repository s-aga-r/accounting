# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_common import create_party


class TestParty(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Party")

    def test_party(self):
        email_id = create_party()
        self.assertTrue(frappe.db.exists(
            {"doctype": "Party", "email_id": email_id}))
