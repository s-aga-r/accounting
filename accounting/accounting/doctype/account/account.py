# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
    @staticmethod
    def get_parent_account(account_name):
        return frappe.db.get_value("Account", account_name, "parent_account")

    @staticmethod
    def get_balance(account_name):
        return frappe.db.get_value("Account", account_name, "balance")

    @staticmethod
    def transfer_amount(from_account, to_account_name, amount):
        if from_account == to_account_name:
            frappe.throw("Debit and Credit Account should not be same.")

        from_account = frappe.get_doc("Account", from_account)

        if from_account.balance >= amount:
            to_account = frappe.get_doc("Account", to_account_name)
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
        else:
            frappe.throw(
                f"Insufficient funds in '{from_account.account_name}' Account.")

    @staticmethod
    def transfer_amount_journal_entry(account_name, credit, debit):
        account = frappe.get_doc("Account", account_name)
        account.balance -= credit
        account.balance += debit
        account.save()
