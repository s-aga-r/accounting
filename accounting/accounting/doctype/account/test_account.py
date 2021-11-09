# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest
from accounting.accounting.doctype.account.account import Account


class TestAccount(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Account")

    def test_account(self):
        Account.create(account_name="Test Account",
                       balance=random.randint(100, 1000))
        self.assertTrue(frappe.db.exists("Account", "Test Account"))
