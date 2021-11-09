# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger


class TestGeneralLedger(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("Accounting Entries")
        frappe.db.delete("Journal Entry")
        frappe.db.delete("General Ledger")

    def test_general_ledger(self):
        journal_entry = create_journal_entry()

        self.assertTrue(
            frappe.db.exists({
                "doctype": "General Ledger",
                "voucher_no": journal_entry.name
            }))


def create_journal_entry():
    journal_entry = frappe.new_doc("Journal Entry")

    party = create_party()
    debit_account, credit_account = create_accounts()

    debit_accounting_entry, credit_accounting_entry = create_accounting_entries(
        debit_account, credit_account, party)

    journal_entry.accounting_entries = [
        debit_accounting_entry,
        credit_accounting_entry,
    ]
    journal_entry.difference = (debit_accounting_entry.debit -
                                credit_accounting_entry.credit)
    journal_entry.insert()

    debit_accounting_entry.parent = credit_accounting_entry.parent = journal_entry.name
    debit_accounting_entry.save()
    credit_accounting_entry.save()

    journal_entry.submit()

    return journal_entry


def create_party():
    Party.create("Test Party", "test_party@example.com")
    return "test_party@example.com"


def create_accounts():
    Account.create("Test Account 1", balance=1000.0)
    Account.create("Test Account 2", balance=1000.0)
    return "Test Account 1", "Test Account 2"


def create_accounting_entries(debit_account, credit_account, party):
    def create_accounting_entry(account, party, debit, credit):
        accounting_entry = frappe.new_doc("Accounting Entries")
        accounting_entry.account = account
        accounting_entry.party = party
        accounting_entry.party_type = "Customer"
        accounting_entry.debit = debit
        accounting_entry.credit = credit
        accounting_entry.transaction_description = None
        accounting_entry.parent = "journal_entry"
        accounting_entry.parentfield = "Accounting Entries"
        accounting_entry.parenttype = "Journal Entry"
        accounting_entry.insert()

        return accounting_entry

    debit_accounting_entry = create_accounting_entry(
        debit_account, party, 500.0, 0.0)
    credit_accounting_entry = create_accounting_entry(
        credit_account, party, 0.0, 500.0)

    return debit_accounting_entry, credit_accounting_entry
