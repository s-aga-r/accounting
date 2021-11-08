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
        frappe.set_user("Administrator")
        # Create the User if not exist with the test_email.
        if not frappe.db.exists("User", test_email):
            create_user()

    def tearDown(self):
        frappe.db.delete("Cart")
        frappe.db.delete("Item")
        frappe.db.delete("Party")

    def test_cart(self):
        item_code = create_item()

        # Remove all items from the Cart if available.
        if Cart.is_exists(test_email):
            Cart.empty(test_email)

        # Add the newly created item to the Cart.
        Cart.add_item(test_email, item_code)

        doc = frappe.get_doc("Cart", test_email)
        self.assertEqual(item_code, doc.items[0].item)


def create_user():
    doc = frappe.new_doc("User")
    doc.email = test_email
    doc.first_name = "Test"
    doc.last_name = "Cart"
    doc.user_type = "Website User"
    doc.flags.ignore_mandatory = True
    doc.insert()


def create_item():
    doc = frappe.new_doc("Item")
    # Assign a random string of 8 characters with prefix "TEST".
    doc.item_code = "TEST" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )
    doc.item_name = "Test Item"
    doc.standard_rate = random.randint(100, 1000)
    doc.image = None
    doc.in_stock = random.randint(1, 10)
    doc.description = "This is a Test Description."
    doc.show_in_products_page = False
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.item_code
