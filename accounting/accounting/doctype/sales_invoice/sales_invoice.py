# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.model.mapper import get_mapped_doc
from datetime import date


class SalesInvoice(Document):
    def validate(self):
        if not self.validate_customer():
            frappe.throw("Select a valid Customer.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if not self.validate_debit_to():
            frappe.throw("Debit To account should be of type Receivable.")
        if not self.validate_income_account():
            frappe.throw("Income Account parent should be of type Income.")
        self.validate_items()
        self.posting_date = today()

    def on_submit(self):
        self.update_stock()
        self.make_gl_entries()

    # Helper Method's

    def validate_customer(self):
        party = frappe.get_doc("Party", self.customer)
        return party.party_type == "Customer"

    def validate_debit_to(self):
        account = frappe.get_doc("Account", self.debit_to)
        return account.account_type == "Receivable"

    def validate_income_account(self):
        account = frappe.get_doc("Account", self.income_account)
        return account.root_type == "Income"

    def validate_items(self):
        items = self.get_filtered_items()
        for item_name, item_qty in items.items():
            item = frappe.get_doc("Item", item_name)
            if item.in_stock < item_qty:
                if item.in_stock == 0:
                    frappe.throw(
                        f"{item.item_name} ({item.name}) is out of stock.")
                else:
                    frappe.throw(
                        f"Only {item.in_stock} {item.item_name} ({item.name}) are in the stock."
                    )

    def get_filtered_items(self):
        items = {}
        for item in self.items:
            if item.item not in items:
                items[item.item] = item.qty
            else:
                items[item.item] += item.qty
        return items

    def update_stock(self):
        items = self.get_filtered_items()
        for item_name, item_qty in items.items():
            item = frappe.get_doc("Item", item_name)
            item.in_stock -= item_qty
            item.save()

    def make_gl_entries(self):
        GeneralLedger.generate_gl_entries(debit_account=self.debit_to, credit_account=self.income_account, transaction_type="Sales Invoice",
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
