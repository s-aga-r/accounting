import frappe


def get_context(context):
    products = frappe.get_all(
        "Item",
        fields=[
            "item_code",
            "item_name",
            "standard_rate",
            "image",
            "in_stock",
        ],
    )

    context.products = products
    context.is_logged_in = frappe.session.user != "Guest"

    return context
