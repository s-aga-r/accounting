// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Accounting Entries', {
	accounting_entries_remove(frm) {
		calc_grand_total(frm);
	},
	debit(frm) {
		calc_grand_total(frm);
	},
	credit(frm) {
		calc_grand_total(frm);
	}
});

function calc_grand_total(frm) {
	var total_debit = 0;
	var total_credit = 0;
	var acc_entries = frm.doc.accounting_entries;
	acc_entries.forEach(function (acc_entry) {
		if (acc_entry.party != null && typeof acc_entry.debit == "number" && typeof acc_entry.credit == "number") {
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
