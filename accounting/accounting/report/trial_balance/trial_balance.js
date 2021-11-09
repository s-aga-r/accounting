// Copyright (c) 2016, Sagar Sharma and contributors
// For license information, please see license.txt
/* eslint-disable */

const date = new Date();
let current_year = date.getFullYear();
let next_year = current_year + 1;

frappe.query_reports['Trial Balance'] = {
	'filters': [
		{
			fieldname: 'filter_based_on',
			label: 'Filter Based On',
			fieldtype: 'Select',
			options: ['Fiscal Year', 'Date Range'],
			default: 'Fiscal Year'
		},
		{
			'fieldname': 'start_year',
			'label': 'Start Year',
			'fieldtype': 'Link',
			'options': 'Fiscal Year',
			default: current_year + '-' + next_year,
		},
		{
			'fieldname': 'end_year',
			'label': 'End Year',
			'fieldtype': 'Link',
			'options': 'Fiscal Year',
			default: current_year + '-' + next_year,
		},
		{
			'fieldname': 'from_date',
			'label': 'From Date',
			'fieldtype': 'Date',
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
		},
		{
			'fieldname': 'to_date',
			'label': 'To Date',
			'fieldtype': 'Date',
			default: frappe.datetime.get_today(),
		}
	]
};
