# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest


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


def create_item():
    doc = frappe.new_doc("Item")
    doc.item_code = "TESTITEM"
    doc.item_name = "Test Item"
    doc.standard_rate = random.randint(100, 1000)
    doc.image = None
    doc.in_stock = random.randint(1, 10)
    doc.description = "This is a Description."
    doc.show_in_products_page = False
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.item_code
