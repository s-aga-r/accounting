// Copyright (c) 2021, Sagar Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on('COA Importer', {
	onload: function (frm) {
		// Make file field empty on Page Load.
		frm.set_value("file", "")
	},
	refresh: function (frm) {
		frm.disable_save();
		frm.add_custom_button("Import", () => {
			frappe.call({
				method: "accounting.accounting.doctype.coa_importer.coa_importer.import_coa",
				args: {
					"file_url": frm.doc.file
				},
				freeze: true,
				callback: function (result) {
					frappe.msgprint(result.message)
				}
			})
		})
	}
});
