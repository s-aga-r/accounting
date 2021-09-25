# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Items(Document):
    def validate(self):
        if self.amount != (self.rate * self.qty):
            frappe.throw("Something went wrong!")
