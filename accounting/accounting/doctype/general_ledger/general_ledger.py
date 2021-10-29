# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear


class GeneralLedger(Document):
    @staticmethod
    def generate_entries(debit_account: str, credit_account: str, voucher_type: str, voucher_no: str, party_type: str, party: str, amount: float) -> None:
        """Create General Ledger entries."""

        # For Credit
        credit_gl = frappe.new_doc("General Ledger")
        credit_gl.posting_date = today()
        credit_gl.voucher_type = voucher_type
        credit_gl.voucher_no = voucher_no
        credit_gl.account = credit_account
        credit_gl.party_type = party_type
        credit_gl.party = party
        credit_gl.debit_amount = 0.0
        credit_gl.credit_amount = amount
        credit_gl.account_balance = Account.get_balance(credit_account)
        credit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        credit_gl.against_account = debit_account
        credit_gl.flags.ignore_permissions = True
        credit_gl.submit()

        # For Debit
        debit_gl = frappe.new_doc("General Ledger")
        debit_gl.posting_date = today()
        debit_gl.voucher_type = voucher_type
        debit_gl.voucher_no = voucher_no
        debit_gl.account = debit_account
        debit_gl.party_type = party_type
        debit_gl.party = party
        debit_gl.debit_amount = amount
        debit_gl.credit_amount = 0.0
        debit_gl.account_balance = Account.get_balance(debit_account)
        debit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        debit_gl.against_account = credit_account
        debit_gl.flags.ignore_permissions = True
        debit_gl.submit()

    @staticmethod
    def generate_entries_for_journal_entry(account: str, voucher_no: str, party_type: str, party: str, debit_amount: float, credit_amount: float) -> None:
        """Create General Ledger entry for Journal Entry."""
        gl = frappe.new_doc("General Ledger")
        gl.posting_date = today()
        gl.voucher_type = "Journal Entry"
        gl.voucher_no = voucher_no
        gl.account = account
        gl.party_type = party_type
        gl.party = party
        gl.debit_amount = debit_amount
        gl.credit_amount = credit_amount
        gl.account_balance = Account.get_balance(account)
        gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        gl.against_account = None
        gl.flags.ignore_permissions = True
        gl.submit()
