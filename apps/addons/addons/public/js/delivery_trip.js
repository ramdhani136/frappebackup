// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Trip', {

	refresh: function (frm) {

		if (frm.doc.docstatus === 0) {
			frm.remove_custom_button('Delivery Note',"Get customers from")
			frm.add_custom_button(__('Delivery Note'), () => {
				erpnext.utils.map_current_doc({
					method: "addons.custom_standard.custom_delivery_trip.make_delivery_trip",
					source_doctype: "Delivery Note",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 0,
						company: frm.doc.company,
					}
				})
			}, __("Get customers from"));
		}
	}
});