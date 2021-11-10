let redirect = (url = "/login") => {
    window.location.href = url;
}

let add_to_cart = (item_code) => {
    frappe.call({
        method: "accounting.accounting.doctype.cart.cart.add_item_to_cart",
        args: {
            "item_code": item_code
        },
        callback: (result) => {
            frappe.show_alert({
                message: __("Added to Cart"),
                indicator: "green"
            }, 5);
        }
    })
}