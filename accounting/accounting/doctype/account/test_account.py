# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest


class TestAccount(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Account")

    def test_account(self):
        account_name = create_account()
        self.assertTrue(frappe.db.exists("Account", account_name))


def create_account():
    doc = frappe.new_doc("Account")
    doc.account_number = "TEST12345"
    doc.account_name = "Test Account"
    doc.balance = random.randint(100, 1000)
    doc.parent_account = None
    doc.root_type = ""
    doc.account_type = ""
    doc.is_group = False
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.account_name
