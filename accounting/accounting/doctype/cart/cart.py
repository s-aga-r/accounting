# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from accounting.accounting.doctype.party.party import Party


class Cart(Document):
    @staticmethod
    def is_exists(customer):
        return frappe.db.exists("Cart", customer)

    @staticmethod
    def create(customer):
        cart = frappe.new_doc("Cart")
        cart.customer = customer
        cart.flags.ignore_permissions = True
        cart.insert()

    @staticmethod
    def add_item(customer, item_code, qty=1):
        if not Party.is_exists(customer):
            user = frappe.get_doc("User", customer)
            Party.create(user.full_name, user.email, user.mobile_no)
        if not Cart.is_exists(customer):
            Cart.create(customer)

        cart = frappe.get_doc("Cart", customer)
        cart.flags.ignore_permissions = True
        item = frappe.get_doc("Item", item_code)

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
    def empty(customer):
        cart = frappe.get_doc("Cart", customer)
        cart.items.clear()
        cart.flags.ignore_permissions = True
        cart.save()


@frappe.whitelist(allow_guest=False)
def add_item_to_cart(item_code, qty=1):
    Cart.add_item(frappe.session.user, item_code, int(qty))
