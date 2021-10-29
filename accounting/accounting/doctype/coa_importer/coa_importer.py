# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import json
import frappe
from pathlib import Path
from frappe.model.document import Document
from accounting.accounting.doctype.account.account import Account

# List of attributes an account(both group and non-group) can have.
account_attributes = ["root_type",
                      "account_type", "account_number", "tax_rate", "report_type"]

# Count the number of accounts created.
count = 0


class COAImporter(Document):
    @staticmethod
    def create_chart(data: dict) -> int:
        """Return the number of accounts created."""

        def create_coa(children: dict, parent: str, root_type: str) -> None:
            """A recursive function to create account(s)."""

            global count
            for account_name, child in children.items():
                if isinstance(child, dict):

                    # Get root_type from child object, return parent's root_type if root_type is empty or undefined in child object.
                    root_type = child.get("root_type", root_type)

                    report_type = child.get("report_type", "")
                    account_number = child.get("account_number", None)
                    balance = child.get("balance", 0.0)
                    account_type = child.get("account_type", None)
                    is_group = 0

                    # Check for parent account.
                    # The account must be a parent account if it has a is_group = 1 attribute or child account(s).
                    if len(set(child.keys() - set(account_attributes))):
                        is_group = 1

                    Account.create(account_name, root_type, account_number,
                                   balance, parent, account_type, is_group, report_type)
                    count += 1

                    create_coa(child, account_name, root_type)

        create_coa(data, None, None)
        return count


@frappe.whitelist()
def import_coa(file_url: str) -> str:
    """A helper function to parse json(from a json file) as a python dict and pass it to the COAImporter.create_chart()."""

    file_doc = frappe.get_doc("File", {"file_url": file_url})

    name, extension = file_doc.get_extension()

    if extension != ".json":
        frappe.throw("Upload a JSON file.")

    json_str = Path(file_doc.get_full_path()).read_text()
    data = json.loads(json_str)

    COAImporter.create_chart(data)

    return "Imported successfully!"
