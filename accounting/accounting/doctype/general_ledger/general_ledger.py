# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear


class GeneralLedger(Document):
    @staticmethod
    def generate_entries(debit_account: str, credit_account: str, voucher_type: str, voucher_no: str, party_type: str, party: str, amount: float, reverse: bool = False) -> None:
        """Create General Ledger entries for both Debit and Credit."""

        # For Credit
        GeneralLedger.generate_entry(
            credit_account, voucher_type, voucher_no, party_type, party, 0.0, amount, debit_account, reverse)

        # For Debit
        GeneralLedger.generate_entry(
            debit_account, voucher_type, voucher_no, party_type, party, amount, 0.0, credit_account, reverse)

    @staticmethod
    def generate_entry(account: str, voucher_type: str, voucher_no: str, party_type: str, party: str, debit_amount: float, credit_amount: float, against_account: str = None, reverse: bool = False):
        """Create General Ledger entry."""

        if reverse:
            account, against_account = against_account, account

        gl = frappe.new_doc("General Ledger")
        gl.posting_date = today()
        gl.voucher_type = voucher_type
        gl.voucher_no = voucher_no
        gl.account = account
        gl.party_type = party_type
        gl.party = party
        gl.debit_amount = debit_amount
        gl.credit_amount = credit_amount
        gl.account_balance = Account.get_balance(account)
        gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        gl.against_account = against_account
        gl.flags.ignore_permissions = True
        gl.submit()
