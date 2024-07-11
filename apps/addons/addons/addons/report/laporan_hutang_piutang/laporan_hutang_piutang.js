// Copyright (c) 2016, PT DAS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Laporan Hutang Piutang"] = {
	"filters": [
		{	
			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"reqd" : 1, 
			"get_query": function() {
				return {
					query: "addons.addons.report.laporan_hutang_piutang.laporan_hutang_piutang.account_able_query"
				}
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
	]
};
