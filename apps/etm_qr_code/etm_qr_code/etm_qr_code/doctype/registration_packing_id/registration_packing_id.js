// Copyright (c) 2022, DAS DEV and contributors
// For license information, please see license.txt

frappe.ui.form.on('Registration Packing ID', {
	refresh: function (frm) {
		cur_frm.events.read_only_if_not_new_doc();
	},

	// End of hooks ------------------------
	read_only_if_not_new_doc: function () {
		if (!cur_frm.is_new()) {
			cur_frm.fields.forEach(function (l) {
				cur_frm.set_df_property(l.df.fieldname, "read_only", 1)
			})
			if (cur_frm.doc.is_in == 0) {
				cur_frm.set_df_property("conversion", "read_only", 0)
			}
			// Permintaan bisa di override is_in dan is_out nya
			cur_frm.set_df_property("is_in", "read_only", 0)
			cur_frm.set_df_property("is_in_name", "read_only", 0)
			cur_frm.set_df_property("is_out", "read_only", 0)
			cur_frm.set_df_property("is_out_name", "read_only", 0)
		}
	},
});
