// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fiscal Year', {
	refresh: (frm) => {
		frm.add_custom_button('Ledger', () => {
			frappe.route_options = {
				'from_date': frm.doc.start_date,
				'to_date': frm.doc.end_date,
			};
			frappe.set_route('query-report', 'General Ledger Report');
		}, 'fa fa-table');
	}
});

