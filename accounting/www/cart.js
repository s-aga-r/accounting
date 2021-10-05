function checkout() {
    frappe.confirm("Are you sure you want to proceed?",
        () => {
            frappe.call({
                method: "accounting.accounting.doctype.sales_order.sales_order.create_order",
                freeze: true,
                callback: function (result) {
                    location.reload();
                }
            })
        }, () => {
            // Close
        })
}

function update_qty(item_code, qty) {
    frappe.call({
        method: "accounting.accounting.doctype.cart.cart.add_item_to_cart",
        args: {
            "item_code": item_code,
            "qty": qty,
        },
        freeze: true,
        callback: function (result) {
            location.reload();
        }
    });
}

function max_qty(in_stock) {
    frappe.msgprint({
        title: __("Message"),
        indicator: "red",
        message: __("You can buy only upto " + in_stock + " unit(s) of this product.")
    });
}
