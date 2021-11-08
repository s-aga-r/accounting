# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account


class TestJournalEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("Journal Entry")

    def test_journal_entry(self):
        journal_entry = create_journal_entry()

        self.assertTrue(
            frappe.db.exists(
                {
                    "doctype": "Journal Entry",
                    "name": journal_entry.name,
                }
            )
        )


def create_journal_entry():
    journal_entry = frappe.new_doc("Journal Entry")

    create_party()
    create_accounts()
    debit_accounting_entry = create_debit_accounting_entry()
    credit_accounting_entry = create_credit_accounting_entry()

    journal_entry.accounting_entries = [
        debit_accounting_entry,
        credit_accounting_entry,
    ]
    journal_entry.difference = (
        debit_accounting_entry.debit - credit_accounting_entry.credit
    )
    journal_entry.insert()

    debit_accounting_entry.parent = credit_accounting_entry.parent = journal_entry.name
    debit_accounting_entry.save()
    credit_accounting_entry.save()

    journal_entry.submit()

    return journal_entry


def create_party():
    Party.create("Test Party", "test_party@example.com")


def create_accounts():
    Account.create("Test Account 1", balance=1000.0)
    Account.create("Test Account 2", balance=1000.0)


def create_debit_accounting_entry():
    debit_accounting_entry = frappe.new_doc("Accounting Entries")
    debit_accounting_entry.account = "Test Account 1"
    debit_accounting_entry.party = "test_party@example.com"
    debit_accounting_entry.party_type = "Customer"
    debit_accounting_entry.debit = 500.0
    debit_accounting_entry.credit = 0.0
    debit_accounting_entry.transaction_description = None
    debit_accounting_entry.parent = "journal_entry"
    debit_accounting_entry.parentfield = "Accounting Entries"
    debit_accounting_entry.parenttype = "Journal Entry"
    debit_accounting_entry.insert()

    return debit_accounting_entry


def create_credit_accounting_entry():
    credit_accounting_entry = frappe.new_doc("Accounting Entries")
    credit_accounting_entry.account = "Test Account 2"
    credit_accounting_entry.party = "test_party@example.com"
    credit_accounting_entry.party_type = "Customer"
    credit_accounting_entry.debit = 0.0
    credit_accounting_entry.credit = 500.0
    credit_accounting_entry.transaction_description = None
    credit_accounting_entry.parent = "journal_entry"
    credit_accounting_entry.parentfield = "Accounting Entries"
    credit_accounting_entry.parenttype = "Journal Entry"
    credit_accounting_entry.insert()

    return credit_accounting_entry
