# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_common import create_sales_order
from accounting.accounting.doctype.sales_invoice.sales_invoice import SalesInvoice


class TestSalesOrder(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Item")
        frappe.db.delete("Items")
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("General Ledger")
        frappe.db.delete("Sales Order")
        frappe.db.delete("Sales Invoice")

    def test_sales_order(self):
        sales_order = create_sales_order()
        sales_invoice = SalesInvoice.generate_invoice(sales_order.name)
        self.assertTrue(frappe.db.exists("Sales Invoice", sales_invoice.name))
