# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
    @staticmethod
    def get_filtered_items(items: list) -> dict:
        """Return a filtered items dict."""
        items_dict = {}
        for item in items:
            if item.item not in items_dict:
                items_dict[item.item] = item.qty
            else:
                items_dict[item.item] += item.qty
        return items_dict

    @staticmethod
    def update_stock(items: list, operation: str) -> None:
        """Increase and decrease the stock while purchase/sales return and sales/purchase return respectively."""
        items_dict = Item.get_filtered_items(items)
        if operation == "increase":
            for item_name, item_qty in items_dict.items():
                item = frappe.get_doc("Item", item_name)
                item.in_stock += item_qty
                item.flags.ignore_permissions = True
                item.save()
        elif operation == "decrease":
            for item_name, item_qty in items_dict.items():
                item = frappe.get_doc("Item", item_name)
                item.in_stock -= item_qty
                item.flags.ignore_permissions = True
                item.save()

    @staticmethod
    def are_items_available(items: list) -> None:
        """Check the items availability."""
        items_dict = Item.get_filtered_items(items)
        for item_name, item_qty in items_dict.items():
            item = frappe.get_doc("Item", item_name)
            if item.in_stock < item_qty:
                if item.in_stock == 0:
                    frappe.throw(
                        f"{item.item_name} ({item.name}) is out of stock.")
                else:
                    frappe.throw(
                        f"Only {item.in_stock} {item.item_name} ({item.name}) are in the stock."
                    )
