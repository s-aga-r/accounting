# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Party(Document):
    @staticmethod
    def is_exists(party: str) -> bool:
        """Return True if Party exist otherwise False."""
        return frappe.db.exists("Party", party)

    @staticmethod
    def create(party_name: str, email_id: str, party_type: str = "Customer", mobile_number: int = None) -> None:
        """Create new Party."""
        party = frappe.new_doc("Party")
        party.party_type = party_type
        party.party_name = party_name
        party.email_id = email_id
        party.mobile_number = mobile_number
        party.flags.ignore_permissions = True
        party.insert()

    @staticmethod
    def get_type(party_name: str) -> str:
        """Return the Party's type."""
        return frappe.db.get_value("Party", party_name, "party_type")
