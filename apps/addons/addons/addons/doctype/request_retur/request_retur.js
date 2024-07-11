// Copyright (c) 2021, PT DAS and contributors
// For license information, please see license.txt
cur_frm.add_fetch("item_code", "item_name", "item_name")
frappe.ui.form.on('Request Retur', {
	refresh: function(frm) {
		frm.set_query("document_type", function(doc, cdt, cdn){
			doc = locals[cdt][cdn];
			return {
				filters: [
					["name","in",["Delivery Note","Purchase Receipt"]]
				]
			};
		});

		if (frm.doc.docstatus == 1){
			if (frm.doc.document_type == "Delivery Note"){

				frm.add_custom_button(__("Delivery Note"), function(){
					frappe.model.open_mapped_doc({
						method: "addons.addons.doctype.request_retur.request_retur.make_sales_return",
						frm: cur_frm
					})
				}, __("Make Return"));
			}

			if (frm.doc.document_type == "Purchase Receipt"){

				frm.add_custom_button(__("Purchase Receipt"), function(frm){
					frappe.model.open_mapped_doc({
						method: "addons.addons.doctype.request_retur.request_retur.make_sales_return",
						frm: cur_frm
					})
				}, __("Make Return"));
			}
		}

		
	},
	document_type: function(frm){
		frm.set_value("document_name","");
		frm.set_query("document_name", function(doc, cdt, cdn){
			doc = locals[cdt][cdn];
			return {
				filters: [
					["docstatus","=",1]
				]
			};
		});
		frm.clear_table("items");
		frm.refresh_fields();

	},
	document_name: function(frm){
		frm.set_query("item_code","items", function(doc,cdt, cdn){
			doc = locals[cdt][cdn];

			return {
				query : "addons.addons.doctype.request_retur.request_retur.related_items",
				filters: {"doctype":cur_frm.doc.document_type, "docname": cur_frm.doc.document_name}
			}
		});
	}
});