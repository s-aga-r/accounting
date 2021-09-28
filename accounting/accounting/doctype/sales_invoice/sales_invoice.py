# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.model.mapper import get_mapped_doc


class SalesInvoice(Document):
    def validate(self):
        if not self.validate_customer():
            frappe.throw("Select a valid Customer.")
        if getdate(self.posting_date) > getdate(self.payment_due_date):
            frappe.throw(
                "Posting Date should be earlier than Payment Due Date.")
        if not self.validate_debit_to():
            frappe.throw("Debit To account should be of type Receivable.")
        if not self.validate_income_account():
            frappe.throw("Income Account parent should be of type Income.")
        self.validate_items()

    def on_submit(self):
        items = self.get_filtered_items()
        for item_name, item_qty in items.items():
            item = frappe.get_doc("Item", item_name)
            item.in_stock -= item_qty
            item.save()

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

    def make_gl_entries(self):
        # Credit
        credit_gl = frappe.new_doc("General Ledger")
        credit_gl.posting_date = today()
        credit_gl.transaction_type = "Sales Invoice"
        credit_gl.transaction_no = self.name
        credit_gl.account = self.income_account
        credit_gl.party_type = "Customer"
        credit_gl.party = self.customer
        credit_gl.debit_amount = 0.0
        credit_gl.credit_amount = self.total_amount
        credit_gl.voucher_no = None
        credit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        credit_gl.against_account = self.debit_to
        credit_gl.submit()

        # Debit
        debit_gl = frappe.new_doc("General Ledger")
        debit_gl.posting_date = today()
        debit_gl.transaction_type = "Sales Invoice"
        debit_gl.transaction_no = self.name
        debit_gl.account = self.debit_to
        debit_gl.party_type = "Customer"
        debit_gl.party = self.customer
        debit_gl.debit_amount = self.total_amount
        debit_gl.credit_amount = 0.0
        debit_gl.voucher_no = None
        debit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        debit_gl.against_account = self.income_account
        debit_gl.submit()


@frappe.whitelist(allow_guest=False)
def generate_invoice(sales_order_name):
    sales_odr = frappe.get_doc("Sales Order", sales_order_name)
    if sales_odr.docstatus == 1:
        sales_inv = get_mapped_doc("Sales Order", sales_order_name,	{
            "Sales Order": {
                "doctype": "Sales Invoice",
                "field_no_map": ["naming_series"]
            },
        })
        sales_inv.submit()
        return "Invoice No : " + sales_inv.name
    return "Submit this form before generating the invoice."
