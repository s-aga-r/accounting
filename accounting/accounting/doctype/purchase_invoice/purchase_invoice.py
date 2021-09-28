# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.fiscal_year.fiscal_year import FiscalYear
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.model.mapper import get_mapped_doc


class PurchaseInvoice(Document):
    def validate(self):
        if not self.validate_supplier():
            frappe.throw("Select a valid Supplier.")
        if getdate(self.posting_date) > getdate(self.payment_due_date):
            frappe.throw(
                "Posting Date should be earlier than Payment Due Date.")
        if not self.validate_credit_to():
            frappe.throw("Credit To account should be of type Payable.")
        if not self.validate_expense_account():
            frappe.throw("Expense Account parent should be of type Expense.")

    def on_submit(self):
        items = self.get_filtered_items()
        for item_name, item_qty in items.items():
            item = frappe.get_doc("Item", item_name)
            item.in_stock += item_qty
            item.save()

        self.make_gl_entries()

    # Helper Method's
    def validate_supplier(self):
        party = frappe.get_doc("Party", self.supplier)
        return party.party_type == "Supplier"

    def validate_credit_to(self):
        account = frappe.get_doc("Account", self.credit_to)
        return account.account_type == "Payable"

    def validate_expense_account(self):
        account = frappe.get_doc("Account", self.expense_account)
        return account.root_type == "Expense"

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
        credit_gl.transaction_type = "Purchase Invoice"
        credit_gl.transaction_no = self.name
        credit_gl.account = self.credit_to
        credit_gl.party_type = "Supplier"
        credit_gl.party = self.supplier
        credit_gl.debit_amount = 0.0
        credit_gl.credit_amount = self.total_amount
        credit_gl.voucher_no = None
        credit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        credit_gl.against_account = self.expense_account
        credit_gl.submit()

        # Debit
        debit_gl = frappe.new_doc("General Ledger")
        debit_gl.posting_date = today()
        debit_gl.transaction_type = "Purchase Invoice"
        debit_gl.transaction_no = self.name
        debit_gl.account = self.expense_account
        debit_gl.party_type = "Supplier"
        debit_gl.party = self.supplier
        debit_gl.debit_amount = self.total_amount
        debit_gl.credit_amount = 0.0
        debit_gl.voucher_no = None
        debit_gl.fiscal_year = FiscalYear.get_current_fiscal_year()
        debit_gl.against_account = self.credit_to
        debit_gl.submit()


@frappe.whitelist(allow_guest=False)
def generate_invoice(purchase_order_name):
    purchase_odr = frappe.get_doc("Purchase Order", purchase_order_name)
    if purchase_odr.docstatus == 1:
        purchase_inv = get_mapped_doc("Purchase Order", purchase_order_name,	{
            "Purchase Order": {
                "doctype": "Purchase Invoice",
                "field_no_map": ["naming_series"]
            },
        })
        purchase_inv.submit()
        return "Invoice No : " + purchase_inv.name
    return "Submit this form before generating the invoice."
