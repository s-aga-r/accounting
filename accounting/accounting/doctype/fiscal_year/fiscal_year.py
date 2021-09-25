# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class FiscalYear(Document):
    def validate(self):
        if getdate(self.start_date) >= getdate(self.end_date):
            frappe.throw("Start Date should be earlier than End Date.")
