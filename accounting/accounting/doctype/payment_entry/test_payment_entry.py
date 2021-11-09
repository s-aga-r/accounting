# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.test_common import create_sales_invoice


class TestPaymentEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Item")
        frappe.db.delete("Items")
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("General Ledger")
        frappe.db.delete("Sales Invoice")
        frappe.db.delete("Payment Entry")

    def test_payment_entry(self):
        sales_invoice = create_sales_invoice()
        payment_entry = create_payment_entry(sales_invoice)
        self.assertTrue(frappe.db.exists("Payment Entry", payment_entry.name))


def create_payment_entry(sales_invoice):
    Account.create("Debtors", balance=100000.0)
    Account.create("Cash", balance=100000.0)

    doc = frappe.new_doc("Payment Entry")
    doc.reference = "Sales Invoice"
    doc.reference_name = sales_invoice.name
    doc.party_type = "Customer"
    doc.party = sales_invoice.customer
    doc.payment_type = "Receive"
    doc.account_paid_from = "Debtors"
    doc.account_paid_to = "Cash"
    doc.amount = sales_invoice.total_amount
    doc.submit()

    return doc
