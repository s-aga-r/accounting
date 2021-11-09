import frappe
import string
import random
from datetime import date
from accounting.accounting.doctype.party.party import Party
from accounting.accounting.doctype.account.account import Account
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger


def create_item():
    doc = frappe.new_doc("Item")
    # Assign a random string of 8 characters with prefix "TEST".
    doc.item_code = "TEST" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )
    doc.item_name = "Test Item"
    doc.standard_rate = random.randint(100, 1000)
    doc.image = None
    doc.in_stock = 10
    doc.description = "This is a Description."
    doc.show_in_products_page = False
    doc.flags.ignore_mandatory = True
    doc.insert()

    return doc.item_code


def create_journal_entry():
    journal_entry = frappe.new_doc("Journal Entry")

    party = create_party()
    Account.create("Test Account 1", balance=1000.0)
    Account.create("Test Account 2", balance=1000.0)
    debit_account, credit_account = "Test Account 1", "Test Account 2"

    debit_accounting_entry, credit_accounting_entry = create_accounting_entries(
        debit_account, credit_account, party)

    journal_entry.accounting_entries = [
        debit_accounting_entry,
        credit_accounting_entry,
    ]
    journal_entry.difference = (debit_accounting_entry.debit -
                                credit_accounting_entry.credit)
    journal_entry.insert()

    debit_accounting_entry.parent = credit_accounting_entry.parent = journal_entry.name
    debit_accounting_entry.save()
    credit_accounting_entry.save()

    journal_entry.submit()

    return journal_entry


def create_party(party_type="Customer"):
    Party.create("Test Party", "test_party@example.com", party_type)
    return "test_party@example.com"


def create_accounting_entries(debit_account, credit_account, party):
    def create_accounting_entry(account, party, debit, credit):
        accounting_entry = frappe.new_doc("Accounting Entries")
        accounting_entry.account = account
        accounting_entry.party = party
        accounting_entry.party_type = "Customer"
        accounting_entry.debit = debit
        accounting_entry.credit = credit
        accounting_entry.transaction_description = None
        accounting_entry.parent = "journal_entry"
        accounting_entry.parentfield = "Accounting Entries"
        accounting_entry.parenttype = "Journal Entry"
        accounting_entry.insert()

        return accounting_entry

    debit_accounting_entry = create_accounting_entry(
        debit_account, party, 500.0, 0.0)
    credit_accounting_entry = create_accounting_entry(
        credit_account, party, 0.0, 500.0)

    return debit_accounting_entry, credit_accounting_entry


def create_sales_invoice():
    doc = frappe.new_doc("Sales Invoice")

    customer = create_party()
    Account.create("Accounts Receivable", is_group=1)
    Account.create("Debit To",
                   balance=100000.0,
                   parent_account="Accounts Receivable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    debit_to, asset_account = "Debit To", "Asset Account"
    items, total_qty, total_amount = create_items(
        "sales_invoice", "Sales Invoice")

    doc.customer = customer
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.debit_to = debit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_sales_order():
    doc = frappe.new_doc("Sales Order")

    customer = create_party()
    Account.create("Accounts Receivable", is_group=1)
    Account.create("Debit To",
                   balance=100000.0,
                   parent_account="Accounts Receivable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    debit_to, asset_account = "Debit To", "Asset Account"
    items, total_qty, total_amount = create_items("sales_order", "Sales Order")

    doc.customer = customer
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.debit_to = debit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_purchase_invoice():
    doc = frappe.new_doc("Purchase Invoice")

    supplier = create_party("Supplier")
    Account.create("Accounts Payable", is_group=1)
    Account.create("Credit To",
                   balance=100000.0,
                   parent_account="Accounts Payable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    credit_to, asset_account = "Credit To", "Asset Account"
    items, total_qty, total_amount = create_items(
        "purchase_invoice", "Purchase Invoice")

    doc.supplier = supplier
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.credit_to = credit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_purchase_order():
    doc = frappe.new_doc("Purchase Order")

    supplier = create_party("Supplier")
    Account.create("Accounts Payable", is_group=1)
    Account.create("Credit To",
                   balance=100000.0,
                   parent_account="Accounts Payable")
    Account.create("Stock Assets", is_group=1)
    Account.create("Asset Account",
                   balance=100000.0,
                   parent_account="Stock Assets")
    credit_to, asset_account = "Credit To", "Asset Account"
    items, total_qty, total_amount = create_items(
        "purchase_order", "Purchase Order")

    doc.supplier = supplier
    doc.payment_due_date = date.today()
    doc.items = items
    doc.total_qty = total_qty
    doc.total_amount = total_amount
    doc.credit_to = credit_to
    doc.asset_account = asset_account
    doc.insert()

    for item in items:
        item.parent = doc.name
        item.save()

    doc.submit()

    return doc


def create_items(parent, parenttype):
    items = []
    total_qty = 0
    total_amount = 0
    for i in range(6):
        doc = frappe.new_doc("Items")
        doc.item = create_item()
        doc.qty = random.randint(1, 10)
        doc.rate = frappe.db.get_value("Item", doc.item, "standard_rate")
        doc.amount = doc.rate * doc.qty
        doc.parent = parent
        doc.parentfield = "Items"
        doc.parenttype = parenttype
        doc.insert()
        items.append(doc)
        total_qty += doc.qty
        total_amount += doc.amount

    return items, total_qty, total_amount
