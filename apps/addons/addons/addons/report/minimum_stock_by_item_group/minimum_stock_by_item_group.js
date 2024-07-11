// Copyright (c) 2016, PT DAS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Minimum Stock By Item Group"] = {
	"filters": [
		{	
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		}
	]
};
