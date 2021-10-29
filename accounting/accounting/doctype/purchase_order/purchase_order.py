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
        if Account.get_parent(self.credit_to) != "Accounts Payable":
            frappe.throw(
                "Credit account parent should be of type Accounts Payable.")
        if not self.validate_asset_account():
            frappe.throw(
                "Asset account parent should be of type Stock Assets or Stock Liabilities.")
        if Account.get_balance(self.credit_to) < self.total_amount:
            frappe.throw("Insufficient funds in Credit Account.")
        self.posting_date = today()

    def validate_asset_account(self) -> bool:
        parent_account = Account.get_parent(self.asset_account)
        return parent_account == "Stock Assets" or parent_account == "Stock Liabilities"
