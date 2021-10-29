import frappe


def get_context(context):
    user = frappe.session.user

    # Redirect user to login page if anonymous(Guest).
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    # If the user has item(s) in his cart.
    if frappe.db.exists("Cart", user):
        cart = frappe.get_doc("Cart", user)

        items = []
        total_amount = 0

        for cart_item in cart.items:
            item = frappe.get_doc("Item", cart_item.item)

            items.append(
                {
                    "code": item.item_code,
                    "name": item.item_name,
                    "image": item.image,
                    "in_stock": item.in_stock,
                    "rate": cart_item.rate,
                    "qty": cart_item.qty,
                    "amount": cart_item.amount,
                }
            )
            total_amount += cart_item.amount

        context.items = items
        context.total_amount = total_amount

    return context
