# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from accounting.accounting.doctype.test_common import create_journal_entry


class TestJournalEntry(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Account")
        frappe.db.delete("Party")
        frappe.db.delete("Accounting Entries")
        frappe.db.delete("Journal Entry")
        frappe.db.delete("General Ledger")

    def test_journal_entry(self):
        journal_entry = create_journal_entry()
        self.assertTrue(
            frappe.db.exists({
                "doctype": "Journal Entry",
                "name": journal_entry.name,
            }))
