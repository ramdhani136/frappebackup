// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors // License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.stock");

frappe.ui.form.on('Stock Entry', {
	refresh: function(frm) {
		frm.remove_custom_button(__('Expired Batches'), __("Get items from"))
		frm.remove_custom_button(__('Material Request'), __("Get items from"))
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Requests'), function() {
				erpnext.utils.map_current_doc({
					method: "addons.custom_standard.custom_material_request.make_stock_entry",
					source_doctype: "Material Request",
					target: frm,
					date_field: "schedule_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						material_request_type: ["in", ["Material Transfer", "Material Issue", "Material Receipt"]],
						status: ["not in", ["Transferred", "Issued"]]
					}
				})
			}, __("Get items from"));
		}
	},
});
