// Copyright (c) 2016, Sagar Sharma and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger Report"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.now_date(), -1)
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.now_date()
		},
		{
			fieldname: "account",
			label: "Account",
			fieldtype: "Link",
			options: "Account",
		},
		{
			fieldname: "voucher_type",
			label: "Voucher Type",
			fieldtype: "Select",
			options: ["", "Sales Invoice", "Purchase Invoice", "Payment Entry", "Journal Entry"]
		},
		{
			fieldname: "voucher_no",
			label: "Voucher No",
			fieldtype: "Data"
		},
		{
			fieldname: "against_account",
			label: "Against Account",
			fieldtype: "Link",
			options: "Account"
		},
		{
			fieldname: "party_type",
			label: "Party Type",
			fieldtype: "Select",
			options: ["", "Customer", "Supplier"]
		},
		{
			fieldname: "party",
			label: "Party",
			fieldtype: "Link",
			options: "Party"
		},
	]
};
