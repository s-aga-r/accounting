import frappe


def is_logged_in():
    user = frappe.session.user

    if user == "Guest":
        return False

    return True


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
    context.is_logged_in = is_logged_in()

    return context
