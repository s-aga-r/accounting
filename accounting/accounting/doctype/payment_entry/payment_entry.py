# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.sales_invoice.sales_invoice import SalesInvoice
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
from accounting.accounting.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice


class PaymentEntry(Document):
    def validate(self):
        if Party.get_type(self.party) != self.party_type:
            frappe.throw(f"Select a valid {self.party_type}.")
        if Account.get_balance(self.account_paid_from) < self.amount:
            frappe.throw("Insufficient funds in Account Paid From.")
        if self.overbilling_error():
            frappe.throw(
                "Please specify a proper amount . Amount must be lesser than invoice amount, non zero and non negative.")
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.account_paid_from, self.account_paid_to, self.amount)
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.account_paid_to, self.account_paid_from, self.amount)
        self.make_gl_entries(reverse=True)

    # Helper Method's

    def overbilling_error(self):
        if self.reference == "Sales Invoice":
            return SalesInvoice.get_billed_amount(self.reference_name) < self.amount
        if self.reference == "Purchase Invoice":
            return PurchaseInvoice.get_billed_amount(self.reference_name) < self.amount

    def make_gl_entries(self, reverse=False):
        if reverse:
            GeneralLedger.generate_entries(debit_account=self.account_paid_from, credit_account=self.account_paid_to, transaction_type="Payment Entry",
                                           transaction_no=self.name, party_type=self.party_type, party=self.party, amount=self.amount)
        else:
            GeneralLedger.generate_entries(debit_account=self.account_paid_to, credit_account=self.account_paid_from, transaction_type="Payment Entry",
                                           transaction_no=self.name, party_type=self.party_type, party=self.party, amount=self.amount)
