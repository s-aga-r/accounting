// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cart', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Items', {
	qty(frm, cdt, cdn) {
		calc_amount(cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calc_amount(cdt, cdn);
	}
});

function calc_amount(cdt, cdn) {
	let item = frappe.get_doc(cdt, cdn);
	item.amount = item.rate * item.qty;
}