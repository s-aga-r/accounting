let checkout = () => {
    frappe.confirm("Are you sure you want to proceed?",
        () => {
            // Yes
            // Display sales invoice in a new window.
            window.open(window.location.protocol + "//" + window.location.host + "/api/method/accounting.accounting.doctype.sales_order.sales_order.create_order");
        }, () => {
            // Close
        })
}

let update_qty = (item_code, qty) => {
    frappe.call({
        method: "accounting.accounting.doctype.cart.cart.add_item_to_cart",
        args: {
            "item_code": item_code,
            "qty": qty,
        },
        freeze: true,
        callback: (result) => {
            location.reload();
        }
    });
}

let max_qty = (in_stock) => {
    frappe.msgprint({
        title: __("Message"),
        indicator: "red",
        message: __("You can buy only upto " + in_stock + " unit(s) of this product.")
    });
}

let remove_item = (item_code) => {
    frappe.call({
        method: "accounting.accounting.doctype.cart.cart.remove_item_from_cart",
        args: {
            "item_code": item_code,
        },
        freeze: true,
        callback: (result) => {
            location.reload();
        }
    });
}

let remove_all_items = () => {
    frappe.confirm("Are you sure you want to proceed?",
        () => {
            // Yes
            frappe.call({
                method: "accounting.accounting.doctype.cart.cart.remove_all_items_from_cart",
                freeze: true,
                callback: (result) => {
                    location.reload();
                }
            });
        }, () => {
            // Close
        })
}