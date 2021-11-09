# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger


class JournalEntry(Document):
    def validate(self):
        if len(self.accounting_entries) < 2:
            frappe.throw("Minimum two Accounting Entries are required.")
        if self.difference != 0:
            frappe.throw("Total Debit must be equal to Total Credit.")
        for acc_entry in self.get("accounting_entries"):
            if acc_entry.debit > 0 and acc_entry.credit > 0:
                frappe.throw(
                    "Cannot Debit and Credit from the same account at once.")
        self.posting_date = today()

    def on_submit(self):
        for acc_entry in self.get("accounting_entries"):
            Account.transfer_amount_journal_entry(
                acc_entry.account, acc_entry.credit, acc_entry.debit)
            self.make_gl_entries(acc_entry)

    def on_cancel(self):
        for acc_entry in self.get("accounting_entries"):
            if acc_entry.debit == 0.0 or acc_entry.credit == 0.0:
                Account.transfer_amount_journal_entry(
                    acc_entry.account, acc_entry.debit, acc_entry.credit)
                self.make_gl_entries(acc_entry, reverse=True)

    def make_gl_entries(self, account_entry: object, reverse: bool = False) -> None:
        """Create General Ledger entry."""

        debit_amount = account_entry.debit
        credit_amount = account_entry.credit

        if reverse:
            debit_amount, credit_amount = credit_amount, debit_amount

        GeneralLedger.generate_entry(
            account_entry.account, "Journal Entry", self.name, account_entry.party_type, account_entry.party, debit_amount, credit_amount)
