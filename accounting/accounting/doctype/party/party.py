# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Party(Document):
    @staticmethod
    def is_exists(party):
        return frappe.db.exists("Party", party)

    @staticmethod
    def create(party_name, email_id, party_type="Customer", mobile_number=None):
        party = frappe.new_doc("Party")
        party.party_type = party_type
        party.party_name = party_name
        party.email_id = email_id
        party.mobile_number = mobile_number
        party.flags.ignore_permissions = True
        party.insert()

    @staticmethod
    def get_type(party_name):
        return frappe.db.get_value("Party", party_name, "party_type")
