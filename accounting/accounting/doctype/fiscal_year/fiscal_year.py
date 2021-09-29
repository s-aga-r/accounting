# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.utils import getdate
from frappe.model.document import Document


class FiscalYear(Document):
    def validate(self):
        if getdate(self.start_date) >= getdate(self.end_date):
            frappe.throw("Start Date should be earlier than End Date.")

    @staticmethod
    def get_current_fiscal_year():
        if frappe.db.count("Fiscal Year") > 0:
            last_fy = frappe.get_last_doc("Fiscal Year")
            if date.today() <= last_fy.end_date:
                return last_fy.name

        current_year = date.today().year
        next_year = current_year + 1
        new_fy = frappe.new_doc("Fiscal Year")
        new_fy.name = new_fy.year_name = f"{current_year}-{next_year}"
        new_fy.start_date = f"{current_year}/04/01"
        new_fy.end_date = f"{next_year}/03/31"
        new_fy.insert()
        return new_fy.name
