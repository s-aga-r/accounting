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


class SalesInvoice(Document):
    def validate(self):
        if Party.get_type(self.customer) != "Customer":
            frappe.throw("Select a valid Customer.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_type(self.debit_to) != "Receivable":
            frappe.throw("Debit To account should be of type Receivable.")
        if Account.get_root_type(self.income_account) != "Income":
            frappe.throw("Income Account parent should be of type Income.")
        if Account.get_balance(self.income_account) < self.total_amount:
            frappe.throw("Insufficient funds in Income Account.")
        Item.are_items_available(self.items)
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.income_account, self.debit_to, self.total_amount)
        Item.update_stock(self.items, "decrease")
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.debit_to, self.income_account, self.total_amount)
        Item.update_stock(self.items, "increase")
        self.make_gl_entries(reverse=True)

    # Helper Method
    def make_gl_entries(self, reverse=False):
        if reverse:
            GeneralLedger.generate_entries(debit_account=self.income_account, credit_account=self.debit_to, transaction_type="Sales Invoice",
                                           transaction_no=self.name, party_type="Customer", party=self.customer, amount=self.total_amount)
        else:
            GeneralLedger.generate_entries(debit_account=self.debit_to, credit_account=self.income_account, transaction_type="Sales Invoice",
                                           transaction_no=self.name, party_type="Customer", party=self.customer, amount=self.total_amount)


@frappe.whitelist(allow_guest=False)
def generate_invoice(sales_order_name):
    sales_odr = frappe.get_doc("Sales Order", sales_order_name)
    if sales_odr.docstatus == 1:
        sales_inv = get_mapped_doc("Sales Order", sales_order_name,	{
            "Sales Order": {
                "doctype": "Sales Invoice",
                "field_no_map": ["naming_series", "posting_date"]
            },
        })
        sales_inv.submit()
        return "Invoice No : " + sales_inv.name
    return "Submit the form before generating the invoice."
