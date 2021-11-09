// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	reference(frm) {
		if (frm.doc.reference == 'Sales Invoice') {
			frm.set_value({
				party_type: 'Customer',
				payment_type: 'Receive',
				account_paid_from: 'Debtors',
				account_paid_to: 'Cash'
			});
		}
		else if (frm.doc.reference == 'Purchase Invoice') {
			frm.set_value({
				party_type: 'Supplier',
				payment_type: 'Pay',
				account_paid_from: 'Cash',
				account_paid_to: 'Creditors'
			});
		}
	},
	refresh: function (frm) {
		frm.set_query('party', function () {
			return {
				filters: {
					party_type: frm.doc.party_type
				}
			};
		});
		frm.set_query('reference', function () {
			return {
				filters: {
					name: ['in', ['Sales Invoice', 'Purchase Invoice']]
				}
			}
		});
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button('Ledger', function () {
				frappe.route_options = {
					'voucher_no': frm.doc.name,
					'from_date': '',
					'to_date': ''
				};
				frappe.set_route('query-report', 'General Ledger Report');
			}, 'fa fa-table');
		}
	}
});
