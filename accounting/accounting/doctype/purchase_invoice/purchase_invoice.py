# Copyright (c) 2021, Sagar Sharma and contributors
# For license information, please see license.txt

from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.model.mapper import get_mapped_doc
from datetime import date


class PurchaseInvoice(Document):
    def validate(self):
        if not self.validate_supplier():
            frappe.throw("Select a valid Supplier.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if not self.validate_credit_to():
            frappe.throw("Credit To account should be of type Payable.")
        if not self.validate_expense_account():
            frappe.throw("Expense Account parent should be of type Expense.")
        self.posting_date = today()

    def on_submit(self):
        self.update_stock()
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

    def update_stock(self):
        items = self.get_filtered_items()
        for item_name, item_qty in items.items():
            item = frappe.get_doc("Item", item_name)
            item.in_stock += item_qty
            item.save()

    def make_gl_entries(self):
        GeneralLedger.generate_gl_entries(debit_account=self.expense_account, credit_account=self.credit_to, transaction_type="Purchase Invoice",
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
