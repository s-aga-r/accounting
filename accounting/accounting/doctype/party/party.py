# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Party(Document):
    @staticmethod
    def get_type(party_name):
        return frappe.db.get_value("Party", party_name, "party_type")
