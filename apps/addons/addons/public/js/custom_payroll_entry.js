// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

var in_progress = false;

frappe.ui.form.on('Payroll Entry', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 0) {
			if(!frm.is_new()) {
				frm.page.clear_primary_action();
				frm.remove_custom_button(__("Get Employees"))
				frm.add_custom_button(__("Get Employee"),
					function() {
						frm.events.get_employee_details(frm);
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

	get_employee_details: function (frm) {
		return frappe.call({
			
			method: 'payroll_addons.custom_standard.custom_payroll_entry.fill_employee_details',
			args: {"self":frm.doc},
			callback: function(r) {
				frm.refresh_fields()
				frm.refresh()
				
			}
		})
	}
});
