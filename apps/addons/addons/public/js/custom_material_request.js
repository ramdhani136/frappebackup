// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// eslint-disable-next-line
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Material Request', {

	refresh: function(frm) {
		if (frm.doc.material_request_type === "Material Receipt") {
			frm.add_custom_button(__("Material Receipt"),
				() => frm.events.make_stock_entry_custom(frm), __('Create'));
		}
		if (frm.doc.docstatus == 0 && frm.doc.status != "Stopped" && frm.doc.workflow_state != "Closed" ){
			frm.add_custom_button(__('Close'),
					() => frm.events.custom_update_status(frm, 'Stopped'));
		}
	},
	make_stock_entry_custom: function(frm) {
		frappe.model.open_mapped_doc({
			method: "addons.custom_standard.custom_material_request.make_stock_entry",
			frm: frm
		});
	},
	custom_update_status: function(frm, stop_status) {
		frappe.call({
			method: 'addons.custom_standard.custom_material_request.custom_update_status',
			args: { name: frm.doc.name, status: stop_status },
			callback(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	},

});
