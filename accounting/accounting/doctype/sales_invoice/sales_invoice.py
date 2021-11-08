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
            frappe.throw("Please select a valid Customer.")
        if getdate(self.payment_due_date) < date.today():
            frappe.throw(
                "Payment Due Date should not be earlier than today's date.")
        if Account.get_parent(self.debit_to) != "Accounts Receivable":
            frappe.throw(
                "Debit account parent should be of type Accounts Receivable.")
        if not self.validate_asset_account():
            frappe.throw(
                "Asset account parent should be of type Stock Assets or Fixed Assets.")
        Item.are_items_available(self.items)
        self.posting_date = today()

    def on_submit(self):
        Account.transfer_amount(
            self.asset_account, self.debit_to, self.total_amount)
        Item.update_stock(self.items, "decrease")
        self.make_gl_entries()

    def on_cancel(self):
        Account.transfer_amount(
            self.debit_to, self.asset_account, self.total_amount)
        Item.update_stock(self.items, "increase")
        self.make_gl_entries(reverse=True)

    @staticmethod
    def get_billed_amount(sales_invoice: str) -> float:
        """Return billed amount for given sales invoice."""
        return frappe.db.get_value("Sales Invoice", sales_invoice, "total_amount")

    @staticmethod
    def generate(sales_order_name: str) -> object:
        """Create and Submit Sales Invoice using Sales Order."""

        sales_odr = frappe.get_doc("Sales Order", sales_order_name)

        # Allow only if Sales Order is submitted.
        if sales_odr.docstatus == 1:
            sales_inv = get_mapped_doc("Sales Order", sales_order_name,	{
                "Sales Order": {
                    "doctype": "Sales Invoice",
                    "field_no_map": ["naming_series", "posting_date"]
                }
            }, ignore_permissions=True)
            sales_inv.flags.ignore_permissions = True
            sales_inv.submit()
            return sales_inv

        frappe.throw("Submit the form before generating the invoice.")

    def validate_asset_account(self) -> bool:
        parent_account = Account.get_parent(self.asset_account)
        return parent_account == "Stock Assets" or parent_account == "Fixed Assets"

    def make_gl_entries(self, reverse: bool = False) -> None:
        """Create General Ledger entry."""

        debit_account = self.debit_to
        credit_account = self.asset_account

        if reverse:
            debit_account, credit_account = credit_account, debit_account

        GeneralLedger.generate_entries(debit_account=debit_account, credit_account=credit_account, voucher_type="Sales Invoice",
                                       voucher_no=self.name, party_type="Customer", party=self.customer, amount=self.total_amount)


@frappe.whitelist(allow_guest=False)
def generate_invoice(sales_order_name: str) -> object:
    """A helper function to call SalesInvoice.generate()."""
    return SalesInvoice.generate(sales_order_name)
