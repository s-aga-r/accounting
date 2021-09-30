// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	refresh: function (frm) {
		frm.set_query("supplier", function () {
			return {
				filters: {
					party_type: "Supplier"
				}
			};
		});
		frm.set_query("credit_to", function () {
			return {
				filters: {
					parent_account: "Accounts Payable"
				}
			}
		});
		frm.set_query("asset_account", function () {
			return {
				filters: {
					parent_account: ["in", ["Stock Assets", "Stock Liabilities"]]
				}
			}
		});
		frm.set_value("payment_due_date", frappe.datetime.now_date());
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
	});
}
