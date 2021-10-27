# Copyright (c) 2013, Sagar Sharma and contributors
# License: MIT. See LICENSE

import frappe
from accounting.accounting.report.financial_statements import get_data, get_columns


def execute(filters=None):
    columns, data = [], []

    if filters.filter_based_on == "Fiscal Year":
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        if start_year:
            filters.pop("start_year")
            filters["from_date"] = frappe.db.get_value(
                "Fiscal Year", start_year, "start_date")
        if end_year:
            filters.pop("end_year")
            filters["to_date"] = frappe.db.get_value(
                "Fiscal Year", end_year, "end_date")

    # Get data by root account type
    asset = get_data("Asset", "Debit", filters.from_date, filters.to_date)
    liability = get_data("Liability", "Credit",
                         filters.from_date, filters.to_date)
    equity = get_data("Equity", "Credit", filters.from_date, filters.to_date)

    # Add data to rows
    data.extend(asset or [])
    data.extend(liability or [])
    data.extend(equity or [])

    # Add columns
    columns = get_columns()

    return columns, data
