import frappe


def get_context(context):
    user = frappe.session.user

    if user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    if frappe.db.exists("Cart", user):
        cart = frappe.get_doc("Cart", user)

        items = []
        total_amount = 0

        for cart_item in cart.items:
            item = frappe.get_doc("Item", cart_item.item)
            items.append(
                {
                    "name": item.item_name,
                    "image": item.image,
                    "rate": cart_item.rate,
                    "qty": cart_item.qty,
                    "amount": cart_item.amount,
                }
            )
            total_amount += cart_item.amount

        context.items = items
        context.total_amount = total_amount

    return context
