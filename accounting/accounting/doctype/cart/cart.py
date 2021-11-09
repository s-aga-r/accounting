# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from accounting.accounting.doctype.party.party import Party


class Cart(Document):
    @staticmethod
    def is_exists(customer: str) -> bool:
        """Return True if customer exist otherwise False."""
        return frappe.db.exists("Cart", customer)

    @staticmethod
    def create(customer: str) -> None:
        """Create new Cart."""
        cart = frappe.new_doc("Cart")
        cart.customer = customer
        cart.flags.ignore_permissions = True
        cart.insert()

    @staticmethod
    def add_item(customer: str, item_code: str, qty: int = 1) -> None:
        """Add given item to Cart."""

        # Create Party if not exist.
        if not Party.is_exists(customer):
            user = frappe.get_doc("User", customer)
            if not user:
                frappe.throw("Something went wrong!")
            Party.create(user.full_name, user.email, user.mobile_no)

        # Create Cart if not exist.
        if not Cart.is_exists(customer):
            Cart.create(customer)

        # Get user's Cart.
        cart = frappe.get_doc("Cart", customer)
        cart.flags.ignore_permissions = True

        # Get the item that is to be added.
        item = frappe.get_doc("Item", item_code)

        # Traverse the Cart items.
        # Increase the Item quantity if found the item that is to be added.
        # Throw's an error if Item quantity is more than the available stock.
        for cart_item in cart.items:
            if cart_item.item == item_code:
                if item.in_stock < (cart_item.qty + qty):
                    frappe.throw(
                        f"You can buy only upto {item.in_stock} unit(s) of this product.")
                cart_item.rate = item.standard_rate
                cart_item.qty += qty
                cart_item.amount = item.standard_rate * cart_item.qty
                cart.save()
                break
        # If a new Item is to be added to the Cart.
        else:
            items = frappe.new_doc("Items")
            items.parent = customer
            items.parentfield = "Items"
            items.parenttype = "Cart"
            items.item = item_code
            items.qty = qty
            items.rate = item.standard_rate
            items.amount = items.rate * items.qty
            items.flags.ignore_permissions = True
            cart.items.append(items)
            cart.save()

    @staticmethod
    def remove_item(customer: str, item_code: str) -> None:
        """Remove a given item from the Cart."""
        cart = frappe.get_doc("Cart", customer)
        for cart_item in cart.items:
            if cart_item.item == item_code:
                cart.items.remove(cart_item)
                break
        cart.flags.ignore_permissions = True
        cart.save()

    @staticmethod
    def empty(customer: str) -> None:
        """Remove all items from the Cart."""
        cart = frappe.get_doc("Cart", customer)
        cart.items.clear()
        cart.flags.ignore_permissions = True
        cart.save()


@frappe.whitelist(allow_guest=False)
def add_item_to_cart(item_code: str, qty: int = 1) -> None:
    """A helper function to call Cart.add_item()."""
    Cart.add_item(frappe.session.user, item_code, int(qty))


@frappe.whitelist(allow_guest=False)
def remove_item_from_cart(item_code: str) -> None:
    """A helper function to call Cart.remove_item()."""
    Cart.remove_item(frappe.session.user, item_code)


@frappe.whitelist(allow_guest=False)
def remove_all_items_from_cart() -> None:
    """A helper function to call Cart.empty()."""
    Cart.empty(frappe.session.user)
