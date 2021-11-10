// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cart', {
	// refresh: (frm) => {

	// }
});

frappe.ui.form.on('Items', {
	qty(frm, cdt, cdn) {
		calculate_amount(cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calculate_amount(cdt, cdn);
	}
});

let calculate_amount = (cdt, cdn) => {
	let item = frappe.get_doc(cdt, cdn);
	item.amount = item.rate * item.qty;
}
