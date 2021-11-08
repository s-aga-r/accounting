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
            frappe.throw(f"Please select a valid {self.party_type}.")
        if self.overbilling_error():
            frappe.throw(
                "Please specify a proper amount. Amount must be lesser than invoice amount, non zero and non negative.")
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.account_paid_from, self.account_paid_to, self.amount)
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.account_paid_to, self.account_paid_from, self.amount)
        self.make_gl_entries(reverse=True)

    def overbilling_error(self) -> bool:
        """Return Overbilling status as True or False."""
        if self.reference == "Sales Invoice":
            return SalesInvoice.get_billed_amount(self.reference_name) < self.amount
        if self.reference == "Purchase Invoice":
            return PurchaseInvoice.get_billed_amount(self.reference_name) < self.amount

    def make_gl_entries(self, reverse: bool = False) -> None:
        """Create General Ledger entry."""

        debit_account = self.account_paid_to
        credit_account = self.account_paid_from

        if reverse:
            debit_account, credit_account = credit_account, debit_account

        GeneralLedger.generate_entries(debit_account=debit_account, credit_account=credit_account, voucher_type="Payment Entry",
                                       voucher_no=self.name, party_type=self.party_type, party=self.party, amount=self.amount)
