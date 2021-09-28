// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Order', {
	refresh: function (frm) {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button('Generate Invoice', () => {
				frappe.call({
					method: "accounting.accounting.doctype.sales_invoice.sales_invoice.generate_invoice",
					args: {
						'sales_order_name': frm.doc.name
					},
					callback: function (result) {
						frappe.msgprint(result.message)
					}
				})
			})
		}
	}
});

frappe.ui.form.on('Items', {
	items_remove(frm) {
		calc_grand_total(frm);
	},
	item(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn);
	},
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn);
	},
});

function calc_amount(frm, cdt, cdn) {
	let item = frappe.get_doc(cdt, cdn);
	if (item.item)
		item.amount = item.rate * item.qty;
	else
		item.rate = item.amount = 0.0;
	calc_grand_total(frm);
}

function calc_grand_total(frm) {
	var total_amount = 0;
	var total_qty = 0;
	var items = frm.doc.items;
	items.forEach(function (item) {
		if (item.item != null && typeof item.qty == "number" && typeof item.amount == "number") {
			total_amount += item.amount;
			total_qty += item.qty;
		}
	});
	frm.set_value({
		total_amount: total_amount,
		total_qty: total_qty
	})
}
