import frappe


def get_context(context):
    user = frappe.session.user

    if user != "Guest" and frappe.db.exists("Cart", user):
        cart = frappe.get_doc("Cart", user)

        if cart:
            items = []
            total = {"Amount": 0}

            for item in cart.items:
                item_properties = frappe.get_doc("Item", item.item)
                amount = item.rate * item.qty  # Need to Implement in DocType
                items.append(
                    {
                        "Name": item_properties.item_name,
                        "Rate": item.rate,
                        "Qty": item.qty,
                        "Amount": amount,
                    }
                )
                total["Amount"] += amount

            context.items = items
            context.total = total

    return context
