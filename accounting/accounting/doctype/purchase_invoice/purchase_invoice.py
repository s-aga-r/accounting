# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.utils import getdate, today
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from accounting.accounting.doctype.item.item import Item
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger


class PurchaseInvoice(Document):
    def validate(self):
        if Party.get_type(self.supplier) != "Supplier":
            frappe.throw("Select a valid Supplier.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_type(self.credit_to) != "Payable":
            frappe.throw("Credit To account should be of type Payable.")
        if Account.get_root_type(self.expense_account) != "Expense":
            frappe.throw("Expense Account parent should be of type Expense.")
        if Account.get_balance(self.credit_to) < self.total_amount:
            frappe.throw("Insufficient funds in Credit Account.")
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.credit_to, self.expense_account, self.total_amount)
        Item.update_stock(self.items, "increase")
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.expense_account, self.credit_to, self.total_amount)
        Item.update_stock(self.items, "decrease")
        self.make_gl_entries(reverse=True)

    # Helper Method
    def make_gl_entries(self, reverse=False):
        if reverse:
            GeneralLedger.generate_entries(debit_account=self.credit_to, credit_account=self.expense_account, transaction_type="Purchase Invoice",
                                           transaction_no=self.name, party_type="Supplier", party=self.supplier, amount=self.total_amount)
        else:
            GeneralLedger.generate_entries(debit_account=self.expense_account, credit_account=self.credit_to, transaction_type="Purchase Invoice",
                                           transaction_no=self.name, party_type="Supplier", party=self.supplier, amount=self.total_amount)


@frappe.whitelist(allow_guest=False)
def generate_invoice(purchase_order_name):
    purchase_odr = frappe.get_doc("Purchase Order", purchase_order_name)
    if purchase_odr.docstatus == 1:
        purchase_inv = get_mapped_doc("Purchase Order", purchase_order_name,	{
            "Purchase Order": {
                "doctype": "Purchase Invoice",
                "field_no_map": ["naming_series", "posting_date"]
            },
        })
        purchase_inv.submit()
        return "Invoice No : " + purchase_inv.name
    return "Submit the form before generating the invoice."
