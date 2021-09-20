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
        filters={"is_active": True},
    )

    context.products = products

    return context
