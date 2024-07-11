frappe.ui.form.on('Quotation', {
	onload: function (frm) {
		frm.set_df_property('taxes_and_charges', 'hidden', 1)
		frm.set_df_property('taxes', 'hidden', 1)
	},
});