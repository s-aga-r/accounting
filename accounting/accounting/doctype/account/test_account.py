# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import string
import random
import unittest


class TestAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        frappe.db.delete("Account")
        print(".Account -> Passed")

    def test_create_account(self):
        frappe.set_user("Administrator")
        doc = frappe.new_doc("Account")
        doc.account_number = "TEST" + "".join(random.choices(string.ascii_uppercase +
                                                             string.digits, k=10))
        doc.account_name = "Test Account " + "".join(random.choices(string.ascii_uppercase +
                                                                    string.digits, k=5))
        doc.balance = random.randint(100, 1000)
        doc.parent_account = None
        doc.root_type = ""
        doc.account_type = ""
        doc.is_group = False
        doc.flags.ignore_mandatory = True
        doc.insert()
        account_number = frappe.db.get_value(
            "Account", doc.account_name, "account_number")

        self.assertEqual(account_number, doc.account_number)
