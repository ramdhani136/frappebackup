// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('API Creation', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('API Creation Action', {
	document_type: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		if (d.document_type) {
			var document_type = d.document_type;
			document_type = document_type.toLowerCase().replace(/ /g, "_");
			d.key = document_type;
			
			frm.refresh_fields();
		}else{
			// tidak melakukan apa apa
		}
	}
});