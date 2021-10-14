# Copyright (c) 2013, Sagar Sharma and contributors
# License: MIT. See LICENSE

import frappe


def execute(filters=None):
    columns, data = [], []

    columns = [
        {
            "fieldname": "posting_date",
            "label": "Posting Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account"
        },
        {
            "fieldname": "debit_amount",
            "label": "Debit (₹)",
            "fieldtype": "Currency",
        },
        {
            "fieldname": "credit_amount",
            "label": "Credit (₹)",
            "fieldtype": "Currency",
        },
        {
            "fieldname": "account_balance",
            "label": "Balance (₹)",
            "fieldtype": "Currency",
        },
        {
            "fieldname": "voucher_type",
            "label": "Voucher Type",
            "fieldtype": "Select",
            "options": "Sales Invoice\nPurchase Invoice\nPayment Entry\nJournal Entry"
        },
        {
            "fieldname": "voucher_no",
            "label": "Voucher No",
            "fieldtype": "Data"
        },
        {
            "fieldname": "against_account",
            "label": "Against Account",
            "fieldtype": "Link",
            "options": "Account"
        },
        {
            "fieldname": "party_type",
            "label": "Party Type",
            "fieldtype": "Select",
            "options": "Customer\nSupplier"
        },
        {
            "fieldname": "party",
            "label": "Party",
            "fieldtype": "Link",
            "options": "Party"
        },
    ]

    if filters:
        from_date = filters.get("from_date", None)
        to_date = filters.get("to_date", None)
        if from_date:
            filters.pop("from_date")
        if to_date:
            filters.pop("to_date")
        filters["posting_date"] = "between", [from_date, to_date]

    data = frappe.get_all(doctype="General Ledger", fields=[
                          "posting_date", "account", "debit_amount", "credit_amount", "account_balance", "voucher_type", "voucher_no", "against_account", "party_type", "party"], filters=filters)

    return columns, data
