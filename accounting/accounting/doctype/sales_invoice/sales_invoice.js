// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: (frm) => {
		frm.set_query('customer', () => {
			return {
				filters: {
					party_type: 'Customer'
				}
			};
		});
		frm.set_query('item', 'items', () => {
			return {
				filters: {
					in_stock: ['>', 0]
				}
			}
		});
		frm.set_query('debit_to', () => {
			return {
				filters: {
					parent_account: 'Accounts Receivable'
				}
			}
		});
		frm.set_query('asset_account', () => {
			return {
				filters: {
					parent_account: ['in', ['Stock Assets', 'Fixed Assets']]
				}
			}
		});
		if (frm.doc.docstatus == 0) {
			frm.set_value('payment_due_date', frappe.datetime.now_date());
		}
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button('Ledger', () => {
				frappe.route_options = {
					'voucher_no': frm.doc.name,
					'from_date': '',
					'to_date': ''
				};
				frappe.set_route('query-report', 'General Ledger Report');
			}, 'fa fa-table');

			frm.add_custom_button('Payment', () => {
				frappe.route_options = {
					'reference': 'Sales Invoice',
					'reference_name': frm.doc.name,
					'party_type': 'Customer',
					'party': frm.doc.customer,
					'payment_type': 'Receive',
					'account_paid_from': 'Debtors',
					'account_paid_to': 'Cash',
					'amount': frm.doc.total_amount,
				};
				frappe.set_route('payment-entry', 'new-payment-entry-1');
			});
		}
	}
});

frappe.ui.form.on('Items', {
	items_remove(frm) {
		calculate_grand_total(frm);
	},
	item(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	qty(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
});

let calculate_amount = (frm, cdt, cdn) => {
	let item = frappe.get_doc(cdt, cdn);
	if (item.item)
		item.amount = item.rate * item.qty;
	else
		item.rate = item.amount = 0.0;
	calculate_grand_total(frm);
}

let calculate_grand_total = (frm) => {
	let total_amount = 0;
	let total_qty = 0;
	let items = frm.doc.items;
	items.forEach((item) => {
		if (item.item != null && typeof item.qty == 'number' && typeof item.amount == 'number') {
			total_amount += item.amount;
			total_qty += item.qty;
		}
	});
	frm.set_value({
		total_amount: total_amount,
		total_qty: total_qty
	});
}