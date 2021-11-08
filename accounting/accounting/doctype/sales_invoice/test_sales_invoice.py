# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import string
import unittest
from datetime import date
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account


class TestSalesInvoice(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Item")
        frappe.db.delete("Items")
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("General Ledger")
        frappe.db.delete("Sales Invoice")

    def test_sales_invoice(self):
        sales_invoice = create_sales_invoice()
        self.assertTrue(frappe.db.exists("Sales Invoice", sales_invoice.name))


def create_sales_invoice():
    doc = frappe.new_doc("Sales Invoice")

    customer = create_customer()
    debit_to, asset_account = create_accounts()
    items, total_qty, total_amount = create_items()

    doc.customer = customer
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.debit_to = debit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_customer():
    Party.create("Test Party", "test_party@example.com")
    return "test_party@example.com"


def create_accounts():
    Account.create("Accounts Receivable", is_group=1)
    Account.create("Debit To",
                   balance=100000.0,
                   parent_account="Accounts Receivable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    return "Debit To", "Asset Account"


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
        doc.parent = "sales_invoice"
        doc.parentfield = "Items"
        doc.parenttype = "Sales Invoice"
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
