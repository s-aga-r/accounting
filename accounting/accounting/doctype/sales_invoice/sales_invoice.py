# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class SalesInvoice(Document):
    def validate(self):
        if not self.validate_customer():
            frappe.throw("Select a valid Customer.")
        if getdate(self.posting_date) > getdate(self.payment_due_date):
            frappe.throw("Posting Date should be earlier than Payment Due Date.")
        if not self.validate_debit_to():
            frappe.throw("Debit To account should be of type Receivable.")
        if not self.validate_income_account():
            frappe.throw("Income Account parent should be of type Income.")

    def validate_customer(self):
        party = frappe.get_doc("Party", self.customer)
        return party.party_type == "Customer"

    def validate_debit_to(self):
        account = frappe.get_doc("Account", self.debit_to)
        return account.account_type == "Receivable"

    def validate_income_account(self):
        account = frappe.get_doc("Account", self.income_account)
        return account.root_type == "Income"
