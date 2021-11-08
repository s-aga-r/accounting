# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
    @staticmethod
    def get_parent(account_name: str) -> str:
        """Return the Parent of a given account."""
        return frappe.db.get_value("Account", account_name, "parent_account")

    @staticmethod
    def get_balance(account_name: str) -> float:
        """Return the Balance of a given account."""
        return frappe.db.get_value("Account", account_name, "balance")

    @staticmethod
    def transfer_amount(from_account_name: str, to_account_name: str, amount: float) -> None:
        """Transfer the amount from one account to another."""

        # Throw's an error if from_account_name is same as to_account_name.
        if from_account_name == to_account_name:
            frappe.throw("Debit and Credit Account must be different.")

        from_account = frappe.get_doc("Account", from_account_name)
        to_account = frappe.get_doc("Account", to_account_name)
        from_account.balance -= amount
        to_account.balance += amount
        from_account.flags.ignore_permissions = True
        from_account.flags.ignore_mandatory = True
        from_account.save()
        to_account.flags.ignore_permissions = True
        to_account.flags.ignore_mandatory = True
        to_account.save()

    @staticmethod
    def transfer_amount_journal_entry(account_name: str, credit: float, debit: float) -> None:
        """Transfer the amount for Journal Entry."""
        account = frappe.get_doc("Account", account_name)
        account.balance -= credit
        account.balance += debit
        account.flags.ignore_mandatory = True
        account.flags.ignore_permissions = True
        account.save()

    @staticmethod
    def create(account_name: str, root_type: str = "", account_number: str = None, balance: float = 0.0, parent_account: str = None, account_type: str = None, is_group: bool = 0, report_type: str = "") -> None:
        """Create new Account."""
        account = frappe.new_doc("Account")
        account.account_number = account_number
        account.account_name = account_name
        account.balance = balance
        account.parent_account = parent_account
        account.root_type = root_type
        account.account_type = account_type
        account.is_group = is_group
        account.report_type = report_type
        account.flags.ignore_mandatory = True
        account.flags.ignore_permissions = True
        account.insert()
