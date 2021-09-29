# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.utils import getdate, today
from frappe.model.document import Document
from accounting.accounting.doctype.item.item import Item
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account


class SalesOrder(Document):
    def validate(self):
        if Party.get_type(self.customer) != "Customer":
            frappe.throw("Select a valid Customer.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_type(self.debit_to) != "Receivable":
            frappe.throw("Debit To account should be of type Receivable.")
        if Account.get_root_type(self.income_account) != "Income":
            frappe.throw("Income Account parent should be of type Income.")
        if Account.get_balance(self.income_account) < self.total_amount:
            frappe.throw("Insufficient funds in Income Account.")
        Item.are_items_available(self.items)
        self.posting_date = today()
