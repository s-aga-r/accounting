# Copyright (c) 2013, Sagar Sharma and contributors
# License: MIT. See LICENSE

import frappe
from frappe.utils import flt
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

    income = get_data("Income", "Credit", filters.from_date, filters.to_date)
    expense = get_data("Expense", "Debit", filters.from_date, filters.to_date)
    net_profit_loss = get_net_profit_loss(income, expense)

    data.extend(income or [])
    data.extend(expense or [])

    if net_profit_loss:
        data.append(net_profit_loss)

    columns = get_columns()

    report_summary = get_report_summary(income, expense, net_profit_loss)

    return columns, data, None, None, report_summary


def get_net_profit_loss(income, expense):
    net_profit_loss = {
        "account_name": "'" + frappe._("Profit for the year") + "'",
        "account": "'" + frappe._("Profit for the year") + "'",
        "warn_if_negative": True
    }

    total_income = flt(income[-2]['opening_balance'], 3)
    total_expense = flt(expense[-2]['opening_balance'], 3)
    net_profit_loss['opening_balance'] = total_income - total_expense

    return net_profit_loss


def get_report_summary(income, expense, net_profit_loss):
    net_income, net_expense, net_profit = 0.0, 0.0, 0.0

    net_income = flt(income[-2]['opening_balance'], 3)
    net_expense = flt(expense[-2]['opening_balance'], 3)
    net_profit = flt(net_profit_loss['opening_balance'], 3)

    profit_label = frappe._("Net Profit")
    income_label = frappe._("Total Income")
    expense_label = frappe._("Total Expense")

    return [
        {
            "value": net_income,
            "label": income_label,
            "datatype": "Currency"
        },
        {"type": "separator", "value": "-"},
        {
            "value": net_expense,
            "label": expense_label,
            "datatype": "Currency"
        },
        {"type": "separator", "value": "=", "color": "blue"},
        {
            "value": net_profit,
            "indicator": "Green" if net_profit > 0 else "Red",
            "label": profit_label,
            "datatype": "Currency"
        }
    ]
