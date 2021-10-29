# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe import get_print
from frappe.model.document import Document
from frappe.utils import getdate, today, add_to_date
from accounting.accounting.doctype.cart.cart import Cart
from accounting.accounting.doctype.item.item import Item
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.sales_invoice.sales_invoice import SalesInvoice


class SalesOrder(Document):
    def validate(self):
        if Party.get_type(self.customer) != "Customer":
            frappe.throw("Select a valid Customer.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_parent(self.debit_to) != "Accounts Receivable":
            frappe.throw(
                "Debit account parent should be of type Accounts Receivable.")
        if not self.validate_asset_account():
            frappe.throw(
                "Asset account parent should be of type Stock Assets or Fixed Assets.")
        if Account.get_balance(self.asset_account) < self.total_amount:
            frappe.throw("Insufficient funds in Asset Account.")
        Item.are_items_available(self.items)
        self.posting_date = today()

    def validate_asset_account(self) -> bool:
        parent_account = Account.get_parent(self.asset_account)
        return parent_account == "Stock Assets" or parent_account == "Fixed Assets"

    @staticmethod
    def create(customer: str, debit_to_account: str = "Debtors", asset_account: str = "Stock In Hand") -> object:
        """Create and Submit Sales Order."""
        cart = frappe.get_doc("Cart", customer)

        total_qty = 0
        total_amount = 0
        for cart_item in cart.items:
            total_qty += cart_item.qty
            total_amount += cart_item.amount

        sales_odr = frappe.new_doc("Sales Order")
        sales_odr.customer = customer
        sales_odr.posting_date = today()
        sales_odr.payment_due_date = add_to_date(today(), days=15)
        sales_odr.items = cart.items
        sales_odr.total_qty = total_qty
        sales_odr.total_amount = total_amount
        sales_odr.debit_to = debit_to_account
        sales_odr.asset_account = asset_account
        sales_odr.flags.ignore_permissions = True
        sales_odr.submit()
        return SalesInvoice.generate(sales_odr.name)


@frappe.whitelist(allow_guest=False)
def create_order() -> None:
    """A helper function to call SalesOrder.create()."""
    customer = frappe.session.user
    sales_inv = SalesOrder.create(customer)
    Cart.empty(customer)
    if sales_inv:
        frappe.local.response.filecontent = get_print(
            sales_inv.doctype, sales_inv.name, doc=sales_inv, print_format="Sales Invoice", as_pdf=True
        )
        frappe.local.response.filename = sales_inv.name + ".pdf"
        frappe.local.response.type = "pdf"
