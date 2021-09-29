# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from accounting.accounting.doctype.account.account import Account
from frappe.model.document import Document
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger


class PaymentEntry(Document):
    def validate(self):
        if frappe.db.get_value("Party", self.party, "party_type") != self.party_type:
            frappe.throw(f"Select a valid {self.party_type}.")
        if Account.get_balance(self.account_paid_from) < self.amount:
            frappe.throw("Insufficient funds in Account Paid From.")

    def on_submit(self):
        Account.transfer_amount(
            self.account_paid_from, self.account_paid_to, self.amount)
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.account_paid_from, self.account_paid_to, self.amount)
        self.make_gl_entries(reverse=True)

    def make_gl_entries(self, reverse=False):
        if reverse:
            GeneralLedger.generate_gl_entries(debit_account=self.account_paid_from, credit_account=self.account_paid_to, transaction_type="Payment Entry",
                                              transaction_no=self.name, party_type=self.party_type, party=self.party, amount=self.amount)
        else:
            GeneralLedger.generate_gl_entries(debit_account=self.account_paid_to, credit_account=self.account_paid_from, transaction_type="Payment Entry",
                                              transaction_no=self.name, party_type=self.party_type, party=self.party, amount=self.amount)
