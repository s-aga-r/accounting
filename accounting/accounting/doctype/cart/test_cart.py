# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import string
import random
import unittest
from accounting.accounting.doctype.cart.cart import Cart

test_email = "test_cart@example.com"


class TestCart(unittest.TestCase):
    def setUp(self):
        if not frappe.db.exists("User", test_email):
            frappe.set_user("Administrator")
            doc = frappe.new_doc("User")
            doc.email = test_email
            doc.first_name = "Test"
            doc.last_name = "Cart"
            doc.user_type = "Website User"
            doc.flags.ignore_mandatory = True
            doc.insert()

    def tearDown(self):
        frappe.db.delete("Cart")
        frappe.db.delete("Item")
        frappe.db.delete("Party")
        print("Cart -> Passed")

    def test_add_item_to_cart(self):
        item_code = None
        frappe.set_user("Administrator")
        doc = frappe.new_doc("Item")
        doc.item_code = item_code = "TEST" + "".join(random.choices(string.ascii_uppercase +
                                                                    string.digits, k=8))
        doc.item_name = "Test Item"
        doc.standard_rate = random.randint(100, 1000)
        doc.image = None
        doc.in_stock = random.randint(1, 10)
        doc.description = "This is a Description."
        doc.show_in_products_page = False
        doc.flags.ignore_mandatory = True
        doc.insert()

        if Cart.is_exists(test_email):
            Cart.empty(test_email)
        Cart.add_item(test_email, item_code)

        doc = frappe.get_doc("Cart", test_email)
        self.assertEqual(item_code, doc.items[0].item)
