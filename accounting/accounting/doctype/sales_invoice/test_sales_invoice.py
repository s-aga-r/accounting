# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_common import create_sales_invoice


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
