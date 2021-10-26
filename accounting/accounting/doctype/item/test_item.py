# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import string
import random
import unittest


class TestItem(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        frappe.db.delete("Item")

    def test_create_item(self):
        frappe.set_user("Administrator")
        doc = frappe.new_doc("Item")
        doc.item_code = "TEST" + "".join(random.choices(string.ascii_uppercase +
                                                        string.digits, k=8))
        doc.item_name = "Test Item"
        doc.standard_rate = random.randint(100, 1000)
        doc.image = None
        doc.in_stock = random.randint(1, 10)
        doc.description = "This is a Description."
        doc.show_in_products_page = False
        doc.flags.ignore_mandatory = True
        doc.insert()
        item_name = frappe.db.get_value("Item", doc.item_code, "item_name")

        self.assertEqual(item_name, doc.item_name)
