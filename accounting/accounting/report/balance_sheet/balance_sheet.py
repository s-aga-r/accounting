# Copyright (c) 2013, Sagar Sharma and contributors
# License: MIT. See LICENSE

import frappe
from datetime import date
from frappe.utils import getdate
from accounting.accounting.report.financial_statements import get_data, get_columns


def execute(filters=None):
    columns, data = [], []

    validate_filters(filters)

    asset = get_data("Asset", "Debit", filters.from_date, filters.to_date)
    liability = get_data("Liability", "Credit",
                         filters.from_date, filters.to_date)
    equity = get_data("Equity", "Credit", filters.from_date, filters.to_date)

    data.extend(asset or [])
    data.extend(liability or [])
    data.extend(equity or [])

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
