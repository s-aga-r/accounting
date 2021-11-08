# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import string
import unittest
from datetime import date
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice


class TestPurchaseOrder(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Item")
        frappe.db.delete("Items")
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("General Ledger")
        frappe.db.delete("Purchase Order")
        frappe.db.delete("Purchase Invoice")

    def test_purchase_order(self):
        purchase_order = create_purchase_order()
        purchase_invoice = PurchaseInvoice.generate(purchase_order.name)
        # self.assertTrue(frappe.db.exists("Purchase Invoice", purchase_invoice))


def create_purchase_order():
    doc = frappe.new_doc("Purchase Order")

    supplier = create_supplier()
    credit_to, asset_account = create_accounts()
    items, total_qty, total_amount = create_items()

    doc.supplier = supplier
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.credit_to = credit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_supplier():
    Party.create("Test Party", "test_party@example.com",
                 party_type="Supplier")
    return "test_party@example.com"


def create_accounts():
    Account.create("Accounts Payable", is_group=1)
    Account.create("Credit To",
                   balance=100000.0,
                   parent_account="Accounts Payable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    return "Credit To", "Asset Account"


def create_items():
    items = []
    total_qty = 0
    total_amount = 0
    for i in range(6):
        doc = frappe.new_doc("Items")
        doc.item = create_item()
        doc.qty = random.randint(1, 10)
        doc.rate = frappe.db.get_value("Item", doc.item, "standard_rate")
        doc.amount = doc.rate * doc.qty
        doc.parent = "purchase_order"
        doc.parentfield = "Items"
        doc.parenttype = "Purchase Order"
        doc.insert()
        items.append(doc)
        total_qty += doc.qty
        total_amount += doc.amount

    return items, total_qty, total_amount


def create_item():
    doc = frappe.new_doc("Item")
    # Assign a random string of 8 characters with prefix "TEST".
    doc.item_code = "TEST" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8))
    # Assign a random string of 5 characters with prefix "Test Item".
    doc.item_name = "Test Item " + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5))
    doc.standard_rate = random.randint(10, 100)
    doc.image = None
    doc.in_stock = 10
    doc.description = "This is a Description."
    doc.show_in_products_page = False
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.item_code
