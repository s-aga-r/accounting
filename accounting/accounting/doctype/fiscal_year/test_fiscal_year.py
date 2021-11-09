# Copyright (c) 2021, Sagar Sharma and Contributors
# See license.txt

import frappe
import unittest
from datetime import date
from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear


class TestFiscalYear(unittest.TestCase):
    def setUp(self):
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.db.delete("Fiscal Year")

    def test_fiscal_year(self):
        current_year = date.today().year
        next_year = current_year + 1
        self.assertEqual(FiscalYear.get_current_fiscal_year(),
                         f"{current_year}-{next_year}")
