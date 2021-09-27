# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class PurchaseOrder(Document):
    def validate(self):
        if not self.validate_supplier():
            frappe.throw("Select a valid Supplier.")
        if getdate(self.posting_date) > getdate(self.payment_due_date):
            frappe.throw(
                "Posting Date should be earlier than Payment Due Date.")
        if not self.validate_credit_to():
            frappe.throw("Credit To account should be of type Payable.")
        if not self.validate_expense_account():
            frappe.throw("Expense Account parent should be of type Expense.")

    # Helper Method's
    def validate_supplier(self):
        party = frappe.get_doc("Party", self.supplier)
        return party.party_type == "Supplier"

    def validate_credit_to(self):
        account = frappe.get_doc("Account", self.credit_to)
        return account.account_type == "Payable"

    def validate_expense_account(self):
        account = frappe.get_doc("Account", self.expense_account)
        return account.root_type == "Expense"
