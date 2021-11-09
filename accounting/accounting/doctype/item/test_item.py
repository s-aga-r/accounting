# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest
from accounting.accounting.doctype.test_common import create_item


class TestItem(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Item")

    def test_item(self):
        item_code = create_item()
        self.assertTrue(
            frappe.db.exists(
                {
                    "doctype": "Item",
                    "item_code": item_code,
                }
            )
        )
