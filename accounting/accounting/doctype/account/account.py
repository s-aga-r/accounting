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
    def transfer_amount(from_account_name, to_account_name, amount):
        if from_account_name == to_account_name:
            frappe.throw("Debit and Credit Account should not be same.")

        from_account = frappe.get_doc("Account", from_account_name)

        if from_account.balance >= amount:
            to_account = frappe.get_doc("Account", to_account_name)
            from_account.balance -= amount
            to_account.balance += amount
            from_account.flags.ignore_permissions = True
            from_account.save()
            to_account.flags.ignore_permissions = True
            to_account.save()
        else:
            frappe.throw(
                f"Insufficient funds in '{from_account.account_name}' Account.")

    @staticmethod
    def transfer_amount_journal_entry(account_name, credit, debit):
        account = frappe.get_doc("Account", account_name)
        account.balance -= credit
        account.balance += debit
        account.flags.ignore_permissions = True
        account.save()

    @staticmethod
    def create(account_name, root_type, account_number=None, balance=0.0, parent_account=None, account_type=None, is_group=0):
        account = frappe.new_doc("Account")
        account.account_number = account_number
        account.account_name = account_name
        account.balance = balance
        account.parent_account = parent_account
        account.root_type = root_type
        account.account_type = account_type
        account.is_group = is_group
        account.flags.ignore_mandatory = True
        account.flags.ignore_permissions = True
        account.insert()
