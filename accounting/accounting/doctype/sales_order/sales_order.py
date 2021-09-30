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
        if Account.get_parent_account(self.debit_to) != "Accounts Receivable":
            frappe.throw(
                "Debit account parent should be of type Accounts Receivable.")
        if not self.validate_asset_account():
            frappe.throw(
                "Asset account parent should be of type Stock Assets or Fixed Assets.")
        if Account.get_balance(self.asset_account) < self.total_amount:
            frappe.throw("Insufficient funds in Asset Account.")
        Item.are_items_available(self.items)
        self.posting_date = today()

    # Helper Method
    def validate_asset_account(self):
        parent_account = Account.get_parent_account(self.asset_account)
        return parent_account == "Stock Assets" or parent_account == "Fixed Assets"
