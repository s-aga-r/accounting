# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear


class GeneralLedger(Document):
    @staticmethod
    def generate_entries(debit_account, credit_account, transaction_type, transaction_no, party_type, party, amount, voucher_no=None):
        # Credit
        credit_gl = frappe.new_doc("General Ledger")
        credit_gl.posting_date = today()
        credit_gl.transaction_type = transaction_type
        credit_gl.transaction_no = transaction_no
        credit_gl.account = credit_account
        credit_gl.party_type = party_type
        credit_gl.party = party
        credit_gl.debit_amount = 0.0
        credit_gl.credit_amount = amount
        credit_gl.account_balance = Account.get_balance(credit_account)
        credit_gl.voucher_no = voucher_no
        credit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        credit_gl.against_account = debit_account
        credit_gl.submit()
        # Debit
        debit_gl = frappe.new_doc("General Ledger")
        debit_gl.posting_date = today()
        debit_gl.transaction_type = transaction_type
        debit_gl.transaction_no = transaction_no
        debit_gl.account = debit_account
        debit_gl.party_type = party_type
        debit_gl.party = party
        debit_gl.debit_amount = amount
        debit_gl.credit_amount = 0.0
        debit_gl.account_balance = Account.get_balance(debit_account)
        debit_gl.voucher_no = voucher_no
        debit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        debit_gl.against_account = credit_account
        debit_gl.submit()
