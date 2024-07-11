// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

var in_progress = false;

frappe.ui.form.on('Payroll Entry', {
	onload: function(frm){
		frm.remove_custom_button(__("Get Employees"))
	},
	refresh: function(frm) {
		if (frm.doc.docstatus == 0) {
			if(!frm.is_new()) {
				frm.page.clear_primary_action();
				frm.remove_custom_button(__("Get Employees"))
				frm.add_custom_button(__("Get Employee"),
					function() {
						// frm.events.get_employee_details_2(frm);
						frappe.call({

							method: 'payroll_addons.custom_standard.custom_payroll_entry.fill_employee_details',
							args: {"self":frm.doc},
							freeze:true,
							callback: function(r) {
								if(frm.doc.employees){
									// frm.save();
									// frm.refresh();
									if(frm.doc.validate_attendance){
										render_employee_attendance(frm, r.message);
									}
								}					
							}	
						})
					}
				).toggleClass('btn-primary', !(frm.doc.employees || []).length);
			}
			if ((frm.doc.employees || []).length) {
				if(!frm.is_new()) {
					frm.page.set_primary_action(__('Create Salary Slip'), () => {
						frm.save('Submit').then(()=>{
							frm.page.clear_primary_action();
							frm.refresh();
							frm.events.refresh(frm);
						});
					});
				}
				else{
					frm.page.set_primary_action(__('Save'), () => {
						frm.save('Save').then(()=>{
							frm.refresh();
							frm.events.refresh(frm);
						});
					});
				}
			}
		}
		if (frm.doc.docstatus == 1) {
			if (frm.custom_buttons) frm.clear_custom_buttons();
			frm.events.add_context_buttons(frm);
		}
	},
	clear_employee_table: function (frm) {
		frm.clear_table('employees');
		if(!frm.is_new()) {
			frm.save();
		}
		frm.refresh();
	},
});
