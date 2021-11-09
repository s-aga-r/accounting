# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_common import create_purchase_order
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
        purchase_invoice = PurchaseInvoice.generate_invoice(
            purchase_order.name, True)
        self.assertTrue(frappe.db.exists(
            "Purchase Invoice", purchase_invoice.name))
