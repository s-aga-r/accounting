# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.utils import getdate, today
from frappe.model.document import Document
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account


class PurchaseOrder(Document):
    def validate(self):
        if Party.get_type(self.supplier) != "Supplier":
            frappe.throw("Select a valid Supplier.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_type(self.credit_to) != "Payable":
            frappe.throw("Credit To account should be of type Payable.")
        if Account.get_root_type(self.expense_account) != "Expense":
            frappe.throw("Expense Account parent should be of type Expense.")
        if Account.get_balance(self.credit_to) < self.total_amount:
            frappe.throw("Insufficient funds in Credit Account.")
        self.posting_date = today()
