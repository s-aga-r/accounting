function checkout() {
    frappe.confirm("Are you sure you want to proceed?",
        () => {
            frappe.call({
                method: "accounting.accounting.doctype.sales_order.sales_order.create_order",
                callback: function (result) {
                    location.reload();
                }
            })
        }, () => {
            // Close
        })
}
