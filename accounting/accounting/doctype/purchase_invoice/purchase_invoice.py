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
            frappe.throw("Please select a valid Supplier.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_parent(self.credit_to) != "Accounts Payable":
            frappe.throw(
                "Credit account parent should be of type Accounts Payable.")
        if not self.validate_asset_account():
            frappe.throw(
                "Asset account parent should be of type Stock Assets or Stock Liabilities.")
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.credit_to, self.asset_account, self.total_amount)
        Item.update_stock(self.items, "increase")
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.asset_account, self.credit_to, self.total_amount)
        Item.update_stock(self.items, "decrease")
        self.make_gl_entries(reverse=True)

    @staticmethod
    def get_billed_amount(purchase_invoice: str) -> float:
        """Return billed amount for given purchase invoice."""
        return frappe.db.get_value("Purchase Invoice", purchase_invoice, "total_amount")

    @staticmethod
    def generate_invoice(purchase_order_name: str, submit: bool = False) -> str:
        """Create and Submit Purchase Invoice using Purchase Order."""

        purchase_odr = frappe.get_doc("Purchase Order", purchase_order_name)

        # Allow only if Purchase Order is submitted.
        if purchase_odr.docstatus == 1:
            purchase_inv = get_mapped_doc("Purchase Order", purchase_order_name,	{
                "Purchase Order": {
                    "doctype": "Purchase Invoice",
                    "field_no_map": ["naming_series", "posting_date"]
                },
            })
            if submit:
                purchase_inv.flags.ignore_permissions = True
                purchase_inv.submit()
            return purchase_inv

        return "Submit the form before generating the invoice."

    def validate_asset_account(self) -> bool:
        parent_account = Account.get_parent(self.asset_account)
        return parent_account == "Stock Assets" or parent_account == "Stock Liabilities"

    def make_gl_entries(self, reverse: bool = False) -> None:
        """Create General Ledger entry."""

        debit_account = self.asset_account
        credit_account = self.credit_to

        GeneralLedger.generate_entries(debit_account=debit_account, credit_account=credit_account, voucher_type="Purchase Invoice",
                                       voucher_no=self.name, party_type="Supplier", party=self.supplier, amount=self.total_amount, reverse=reverse)


@frappe.whitelist(allow_guest=False)
def generate_invoice(purchase_order_name: str) -> str:
    """A helper function to call PurchaseInvoice.generate_invoice()."""
    return PurchaseInvoice.generate_invoice(purchase_order_name)
