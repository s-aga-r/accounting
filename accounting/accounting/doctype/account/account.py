# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
    @staticmethod
    def get_balance(account_name):
        return frappe.db.get_value("Account", account_name, "balance")

    @staticmethod
    def transfer_amount(from_account_name, to_account_name, amount):
        from_account = frappe.get_doc("Account", from_account_name)

        if from_account.balance >= amount:
            to_account = frappe.get_doc("Account", to_account_name)
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
        else:
            frappe.throw(
                f"Insufficient funds in '{from_account.account_name}' Account.")
