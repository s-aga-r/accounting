# Copyright (c) 2013, Sagar Sharma and contributors
# License: MIT. See LICENSE

import frappe
from datetime import date
from frappe.utils import getdate, flt
from accounting.accounting.report.financial_statements import filter_accounts, set_gl_entries_by_account

value_fields = ("opening_debit", "opening_credit", "debit",
                "credit", "closing_debit", "closing_credit")


def execute(filters=None):
    columns, data = [], []
    validate_filters(filters)
    data = get_data(filters)
    columns = get_columns()
    return columns, data


def validate_filters(filters):
    if filters.filter_based_on == "Fiscal Year":

        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)

        if start_year:
            filters.pop("start_year")
            filters["from_date"] = frappe.db.get_value(
                "Fiscal Year", start_year, "start_date")
        else:
            frappe.throw("Please select Start Year.")

        if end_year:
            filters.pop("end_year")
            filters["to_date"] = frappe.db.get_value(
                "Fiscal Year", end_year, "end_date")
        else:
            filters["to_date"] = frappe.db.get_value(
                "Fiscal Year", start_year, "end_date")

    elif filters.filter_based_on == "Date Range":

        from_date = filters.get("from_date", None)
        to_date = filters.get("to_date", None)

        if not from_date:
            frappe.throw("Please select From Date.")
        else:
            if not to_date:
                filters["to_date"] = to_date = date.today()

            if getdate(from_date) > getdate(to_date):
                frappe.throw("From Date cannot be greater than To Date.")


def get_data(filters):
    accounts = frappe.db.sql("""select name, account_number, parent_account, account_name, account_type, lft, rgt
		from `tabAccount` order by lft""", as_dict=True)
    if not accounts:
        return None
    accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)

    min_lft, max_rgt = frappe.db.sql(
        """select min(lft), max(rgt) from `tabAccount`""")[0]
    gl_entries_by_account = {}
    opening_balances = get_opening_balances(filters)
    set_gl_entries_by_account(gl_entries_by_account,
                              filters.from_date, filters.to_date, min_lft, max_rgt)

    total_row = calculate_values(
        accounts, gl_entries_by_account, opening_balances, filters)
    accumulate_values_into_parents(accounts, accounts_by_name)

    data = prepare_data(accounts, filters, total_row, parent_children_map)

    return data


def get_opening_balances(filters):
    opening = get_rootwise_opening_balances(filters)
    return opening


def get_rootwise_opening_balances(filters):
    gle = frappe.db.sql("""
		select
			account, sum(debit_amount) as opening_debit, sum(credit_amount) as opening_credit
		from `tabGeneral Ledger`
		where
		   (posting_date < %(from_date)s)
		group by account""",
                        {
                            "from_date": filters.from_date,
                        },
                        as_dict=True)
    opening = frappe._dict()
    for d in gle:
        opening.setdefault(d.account, d)
    return opening


def calculate_values(accounts, gl_entries_by_account, opening_balances, filters):
    init = {
        "opening_debit": 0.0,
        "opening_credit": 0.0,
        "debit": 0.0,
        "credit": 0.0,
        "closing_debit": 0.0,
        "closing_credit": 0.0
    }

    total_row = {
        "account": "'" + frappe._("Total") + "'",
        "account_name": "'" + frappe._("Total") + "'",
        "warn_if_negative": True,
        "opening_debit": 0.0,
        "opening_credit": 0.0,
        "debit": 0.0,
        "credit": 0.0,
        "closing_debit": 0.0,
        "closing_credit": 0.0,
        "parent_account": None,
        "indent": 0,
        "has_value": True,
    }

    for d in accounts:
        d.update(init.copy())
        d["opening_debit"] = opening_balances.get(
            d.name, {}).get("opening_debit", 0)
        d["opening_credit"] = opening_balances.get(
            d.name, {}).get("opening_credit", 0)

        for entry in gl_entries_by_account.get(d.name, []):
            d["debit"] += flt(entry.debit_amount)
            d["credit"] += flt(entry.credit_amount)
            diff = d["debit"] - d["credit"]

        d["closing_debit"] = d["opening_debit"] + d["debit"]
        d["closing_credit"] = d["opening_credit"] + d["credit"]
        total_row["debit"] += d["debit"]
        total_row["credit"] += d["credit"]

        if d["account_type"] == "Asset" or d["account_type"] == "Expense":
            d["opening_debit"] -= d["opening_credit"]
            d["opening_credit"] = 0.0
            total_row["opening_debit"] += d["opening_debit"]
        if d["account_type"] == "Liability" or d["account_type"] == "Income":
            d["opening_credit"] -= d["opening_debit"]
            d["opening_debit"] = 0.0
            total_row["opening_credit"] += d["opening_credit"]
        if d["account_type"] == "Asset" or d["account_type"] == "Expense":
            d["closing_debit"] -= d["closing_credit"]
            d["closing_credit"] = 0.0
            total_row["closing_debit"] += d["closing_debit"]
        if d["account_type"] == "Liability" or d["account_type"] == "Income":
            d["closing_credit"] -= d["closing_debit"]
            d["closing_debit"] = 0.0
            total_row["closing_credit"] += d["closing_credit"]
    return total_row


def accumulate_values_into_parents(accounts, accounts_by_name):
    for d in reversed(accounts):
        if d.parent_account:
            for key in value_fields:
                accounts_by_name[d.parent_account][key] += d[key]


def prepare_data(accounts, filters, total_row, parent_children_map):
    data = []
    for d in accounts:
        has_value = False
        row = {
            "account": d.name,
            "parent_account": d.parent_account,
            "indent": d.indent,
            "from_date": filters.from_date,
            "to_date": filters.to_date,
            "account_name": ('{} - {}'.format(d.account_number, d.account_name)
                             if d.account_number else d.account_name)
        }
        prepare_opening_and_closing(d)

        for key in value_fields:
            row[key] = flt(d.get(key, 0.0), 3)

            if abs(row[key]) >= 0.005:
                has_value = True

        row["has_value"] = has_value
        data.append(row)

    data.extend([{}, total_row])
    return data


def prepare_opening_and_closing(d):
    d["closing_debit"] = d["opening_debit"] + d["debit"]
    d["closing_credit"] = d["opening_credit"] + d["credit"]
    if d["account_type"] == "Asset" or d["account_type"] == "Expense":
        d["opening_debit"] -= d["opening_credit"]
        d["opening_credit"] = 0.0
    if d["account_type"] == "Liability" or d["account_type"] == "Income":
        d["opening_credit"] -= d["opening_debit"]
        d["opening_debit"] = 0.0
    if d["account_type"] == "Asset" or d["account_type"] == "Expense":
        d["closing_debit"] -= d["closing_credit"]
        d["closing_credit"] = 0.0
    if d["account_type"] == "Liability" or d["account_type"] == "Income":
        d["closing_credit"] -= d["closing_debit"]
        d["closing_debit"] = 0.0


def get_columns():
    return [
        {
            "fieldname": "account",
            "label": frappe._("Account"),
            "fieldtype": "Link",
            "options": "Account",
            "width": 300
        },
        {
            "fieldname": "opening_debit",
            "label": frappe._("Opening (Dr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "fieldname": "opening_credit",
            "label": frappe._("Opening (Cr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "fieldname": "debit",
            "label": frappe._("Debit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "fieldname": "credit",
            "label": frappe._("Credit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "fieldname": "closing_debit",
            "label": frappe._("Closing (Dr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        },
        {
            "fieldname": "closing_credit",
            "label": frappe._("Closing (Cr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        }
    ]
