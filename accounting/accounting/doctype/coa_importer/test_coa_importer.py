# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import random
import unittest
from accounting.accounting.doctype.coa_importer.coa_importer import COAImporter

TEST_ACCOUNTS = {"Application of Funds (Assets)": {"Current Assets": {"Accounts Receivable": {"Debtors": {"account_type": "Receivable"}}, "Bank Accounts": {"account_type": "Bank", "is_group": 1}, "Cash In Hand": {"Cash": {"account_type": "Cash"}, "account_type": "Cash"}, "Loans and Advances (Assets)": {"Employee Advances": {}}, "Securities and Deposits": {"Earnest Money": {}}, "Stock Assets": {"Stock In Hand": {"account_type": "Stock"}, "account_type": "Stock"}, "Tax Assets": {"is_group": 1}}, "Fixed Assets": {"Capital Equipments": {"account_type": "Fixed Asset"}, "Electronic Equipments": {"account_type": "Fixed Asset"}, "Furnitures and Fixtures": {"account_type": "Fixed Asset"}, "Office Equipments": {"account_type": "Fixed Asset"}, "Plants and Machineries": {"account_type": "Fixed Asset"}, "Buildings": {"account_type": "Fixed Asset"}, "Softwares": {"account_type": "Fixed Asset"}, "Accumulated Depreciation": {"account_type": "Accumulated Depreciation"}, "CWIP Account": {"account_type": "Capital Work in Progress"}}, "Investments": {"is_group": 1}, "Temporary Accounts": {"Temporary Opening": {"account_type": "Temporary"}}, "root_type": "Asset"}, "Expenses": {"Direct Expenses": {"Stock Expenses": {"Cost of Goods Sold": {"account_type": "Cost of Goods Sold"}, "Expenses Included In Asset Valuation": {"account_type": "Expenses Included In Asset Valuation"}, "Expenses Included In Valuation": {"account_type": "Expenses Included In Valuation"}, "Stock Adjustment": {"account_type": "Stock Adjustment"}}}, "Indirect Expenses": {"Administrative Expenses": {
}, "Commission on Sales": {}, "Depreciation": {"account_type": "Depreciation"}, "Entertainment Expenses": {}, "Freight and Forwarding Charges": {"account_type": "Chargeable"}, "Legal Expenses": {}, "Marketing Expenses": {"account_type": "Chargeable"}, "Miscellaneous Expenses": {"account_type": "Chargeable"}, "Office Maintenance Expenses": {}, "Office Rent": {}, "Postal Expenses": {}, "Print and Stationery": {}, "Round Off": {"account_type": "Round Off"}, "Salary": {}, "Sales Expenses": {}, "Telephone Expenses": {}, "Travel Expenses": {}, "Utility Expenses": {}, "Write Off": {}, "Exchange Gain/Loss": {}, "Gain/Loss on Asset Disposal": {}}, "root_type": "Expense"}, "Income": {"Direct Income": {"Sales": {}, "Service": {}}, "Indirect Income": {"is_group": 1}, "root_type": "Income"}, "Source of Funds (Liabilities)": {"Current Liabilities": {"Accounts Payable": {"Creditors": {"account_type": "Payable"}, "Payroll Payable": {}}, "Stock Liabilities": {"Stock Received But Not Billed": {"account_type": "Stock Received But Not Billed"}, "Asset Received But Not Billed": {"account_type": "Asset Received But Not Billed"}}, "Duties and Taxes": {"account_type": "Tax", "is_group": 1}, "Loans (Liabilities)": {"Secured Loans": {}, "Unsecured Loans": {}, "Bank Overdraft Account": {}}}, "root_type": "Liability"}, "Equity": {"Capital Stock": {"account_type": "Equity"}, "Dividends Paid": {"account_type": "Equity"}, "Opening Balance Equity": {"account_type": "Equity"}, "Retained Earnings": {"account_type": "Equity"}, "root_type": "Equity"}}


class TestCOAImporter(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")
        frappe.db.delete("Account")

    def tearDown(self):
        frappe.db.delete("Account")

    def test_coa_importer(self):
        count = COAImporter.create_chart(TEST_ACCOUNTS)
        self.assertEqual(count, frappe.db.count("Account"))

        account_name, account_properties = random.choice(
            list(TEST_ACCOUNTS.items()))
        self.assertTrue(frappe.db.exists({
            "doctype": "Account",
            "account_name": account_name,
            "root_type": account_properties.get("root_type", None)
        }))
