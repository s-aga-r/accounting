// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	refresh: (frm) => {
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button('Ledger', () => {
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

frappe.ui.form.on('Accounting Entries', {
	accounting_entries_remove(frm) {
		calculate_grand_total(frm);
	},
	debit(frm) {
		calculate_grand_total(frm);
	},
	credit(frm) {
		calculate_grand_total(frm);
	}
});

let calculate_grand_total = (frm) => {
	let total_debit = 0;
	let total_credit = 0;
	let acc_entries = frm.doc.accounting_entries;
	acc_entries.forEach((acc_entry) => {
		if (acc_entry.party != null && typeof acc_entry.debit == 'number' && typeof acc_entry.credit == 'number') {
			total_debit += acc_entry.debit;
			total_credit += acc_entry.credit;
		}
	});
	frm.set_value({
		total_debit: total_debit,
		total_credit: total_credit,
		difference: total_debit - total_credit
	})
}
