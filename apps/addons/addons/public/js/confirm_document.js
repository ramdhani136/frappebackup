frappe.ui.form.on('Confirmation Document', {
	refresh(frm) {
	    
	    if(frm.doc.amended_from && frm.doc.__islocal){
	        frm.set_value("document_number", "")
            frm.set_value("items", [])
            frm.set_value("pr_items", [])
            frm.set_value("is_return", "")
            frm.set_value("tipe_stock", "")
            frm.set_value("customer", "")
            frm.set_value("supplier", "")
            frm.set_value("tipe_stock", "")
	    }
		if(frm.doc.chosen_type == "Stock Entry"){
			 frm.set_query("document_number", function() {
    			return {
    				query: "addons.custom_standard.custom_confirmation_document.get_stock_entry_for_confirmation_document",
    			};
    		});
		}
		else{
			frm.set_query("document_number", function() {
    			return {
    			    filters:{
    			        "docstatus": 0
    			    }
    			};
    		});
		}
		
		if(frm.doc.tipe_stock == "Out"){
			var level_1 = 0
			var level_2 = 0
			var level_3 = 0
			var level_4 = 0
			var level_5 = 0
	 		for(var row in frm.doc.items){	
				if(!frm.doc.items[row].check_rencana_kirim){
					level_1 = 1
				}
				if(!frm.doc.items[row].checking_stock){
					level_2 = 1
				}
				if(!frm.doc.items[row].check_qty_muat){
					level_3 = 1
				}
				if(!frm.doc.items[row].check_validasi){
					level_4 = 1
				}
				if(!frm.doc.items[row].check_konfirmasi){
					level_5 = 1
				}

	            cur_frm.doc.in_1 = 0
	            cur_frm.doc.in_2 = 0
	            cur_frm.doc.in_3 = 0
	            cur_frm.doc.in_4 = 0
	            cur_frm.doc.in_5 = 0
			}

			if(level_1 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[1])){   
							var df = frappe.meta.get_docfield("Confirmation Document Item","check_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;

				            cur_frm.doc.in_1 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					}
				})
			}
			else if(level_1 == 0 && level_2 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item","check_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;
				            
				            cur_frm.doc.in_1 = 1
				            cur_frm.refresh_fields()
				            
					    }
					    if(frappe.user.has_role(r.message[1])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item","checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","qty_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;     
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            
				            cur_frm.doc.in_2 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					}
				})
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 1){
				console.log("ADS")
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					       	var df = frappe.meta.get_docfield("Confirmation Document Item","checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","qty_rencana_kirim", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_checking_stock", cur_frm.doc.name);
				            df.read_only = 0;

				            cur_frm.doc.in_2 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
					        
					        var df = frappe.meta.get_docfield("Confirmation Document Item","check_qty_muat", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","qty_muat", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_muat", cur_frm.doc.name);
				            df.read_only = 0;

				            cur_frm.doc.in_3 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					    if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
	                	    frm.page.set_primary_action(__('Reject'), () => {
	                			for(var row in frm.doc.items){
	                				frm.doc.items[row].checking_stock = 0
	                				frm.doc.items[row].check_qty_muat = 0
	                				frm.doc.items[row].check_validasi = 0
	                				frm.doc.items[row].check_konfirmasi = 0
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
									},
									freeze_message: "Saving"
								});
	                		}).addClass("btn-danger");
	                	}
					}
				})
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 0 && level_4 == 1){
        
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item","check_qty_muat", cur_frm.doc.name);
            	            df.read_only = 0;
            	            var df = frappe.meta.get_docfield("Confirmation Document Item","qty_muat", cur_frm.doc.name);
            	            df.read_only = 0;
            	            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_muat", cur_frm.doc.name);
            	            df.read_only = 0;

				            cur_frm.doc.in_3 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item","check_validasi", cur_frm.doc.name);
            	            df.read_only = 0;
            	            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_validasi", cur_frm.doc.name);
            	            df.read_only = 0;

				            cur_frm.doc.in_4 = 1
				            cur_frm.refresh_fields()
					    }
					   cur_frm.page.actions_btn_group.hide()
					    if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
	                	
	                	    frm.page.set_primary_action(__('Reject'), () => {
	                			for(var row in frm.doc.items){
	                				frm.doc.items[row].check_qty_muat = 0
	                				frm.doc.items[row].check_validasi = 0
	                				frm.doc.items[row].check_konfirmasi = 0
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
									},
									freeze_message: "Saving"
								});

	                		}).addClass("btn-danger");
	                	}
	    
					}
				})
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 0 && level_4 == 0 && level_5 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item","check_validasi", cur_frm.doc.name);
            	            df.read_only = 0;
            	            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_validasi", cur_frm.doc.name);
            	            df.read_only = 0;

				            cur_frm.doc.in_4 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
					       	var df = frappe.meta.get_docfield("Confirmation Document Item","check_konfirmasi", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item","keterangan_konfirmasi", cur_frm.doc.name);
				            df.read_only = 0;

				            cur_frm.doc.in_5 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					    if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
		                	
	                	    frm.page.set_primary_action(__('Reject'), () => {
	                			for(var row in frm.doc.items){
	                				frm.doc.items[row].check_validasi = 0
	                				frm.doc.items[row].check_konfirmasi = 0
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
									},
									freeze_message: "Saving"
								});

	                		}).addClass("btn-danger");
	                	}
					}
				})
			}
		}

		else if(frm.doc.tipe_stock == "In"){
			var level_1 = 0
			var level_2 = 0
			var level_3 = 0
			var level_4 = 0
			var level_5 = 0
	 		for(var row in frm.doc.pr_items){	
				if(!frm.doc.pr_items[row].check_rencana_bongkar){
					level_1 = 1
				}
				if(!frm.doc.pr_items[row].checking_stock){
					level_2 = 1
				}
				if(!frm.doc.pr_items[row].check_qty_terima){
					level_3 = 1
				}
				if(!frm.doc.pr_items[row].check_review){
					level_4 = 1
				}
				if(!frm.doc.pr_items[row].check_konfirmasi){
					level_5 = 1
				}
			}

			cur_frm.doc.in_1 = 0
            cur_frm.doc.in_2 = 0
            cur_frm.doc.in_3 = 0
            cur_frm.doc.in_4 = 0
            cur_frm.doc.in_5 = 0

			if(level_1 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[1])){   
							var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_rencana_bongkar", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_rencana_bongkar", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_1 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					}
				})
			}
			else if(level_1 == 0 && level_2 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					       var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_rencana_bongkar", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_rencana_bongkar", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_1 = 1
				            cur_frm.refresh_fields()

					    }
					    if(frappe.user.has_role(r.message[1])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item PR","checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","qty_rencana_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_2 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()

					}
				})
				
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					       var df = frappe.meta.get_docfield("Confirmation Document Item PR","checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_checking_stock", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_2 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_qty_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","qty_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_3 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					     if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
	                	
	                	    frm.page.set_primary_action(__('Reject'), () => {
	                			for(var row in frm.doc.pr_items){   			

	                				frm.doc.pr_items[row].checking_stock = 0	
	                				frm.doc.pr_items[row].check_qty_terima = 0
	                				frm.doc.pr_items[row].check_review = 0
	                				frm.doc.pr_items[row].check_konfirmasi = 0
	                				
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
										
									},
									freeze_message: "Saving"
								});
	                		}).addClass("btn-danger");
	                	}
					}
				})

				
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 0 && level_4 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
					        var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_qty_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","qty_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_terima", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_3 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
							var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_review", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_review", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_4 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					     if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
	                	
	                	    frm.page.set_primary_action(__('Reject'), () => {
	                			for(var row in frm.doc.pr_items){   				
	                				frm.doc.pr_items[row].check_qty_terima = 0
	                				frm.doc.pr_items[row].check_review = 0
	                				frm.doc.pr_items[row].check_konfirmasi = 0
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
									},
									freeze_message: "Saving"
								});
	                		}).addClass("btn-danger");
	                	}
					}
				})
			}
			else if(level_1 == 0 && level_2 == 0 && level_3 == 0 && level_4 == 0 && level_5 == 1){
				frappe.call({
					method: 'addons.custom_standard.custom_confirmation_document.get_previous_role',
					args: {
						"workflow_state":frm.doc.workflow_state
					},
					callback: function(r) {
					    console.log(r.message)
					    if(frappe.user.has_role(r.message[0])){
							var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_review", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_review", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_4 = 1
				            cur_frm.refresh_fields()
					    }
					    if(frappe.user.has_role(r.message[1])){
							var df = frappe.meta.get_docfield("Confirmation Document Item PR","check_konfirmasi", cur_frm.doc.name);
				            df.read_only = 0;
				            var df = frappe.meta.get_docfield("Confirmation Document Item PR","keterangan_konfirmasi", cur_frm.doc.name);
				            df.read_only = 0;
				            cur_frm.doc.in_5 = 1
				            cur_frm.refresh_fields()
					    }
					    cur_frm.page.actions_btn_group.hide()
					     if(frappe.user.has_role(r.message[0]) || frappe.user.has_role(r.message[1])){
	                	
	                	    frm.page.set_primary_action(__('Reject'), () => {

	                			for(var row in frm.doc.pr_items){
	                				frm.doc.pr_items[row].check_review = 0
	                				frm.doc.pr_items[row].check_konfirmasi = 0
	                			}
	                			cur_frm.refresh_fields()
	                			frappe.call({
									method: "frappe.desk.form.save.savedocs",
									args: { doc: frm.doc, action: "Save" },
									callback: function (r) {
										$(document).trigger("save", [frm.doc]);
										cur_frm.refresh()
									},
									freeze_message: "Saving"
								});
	                		}).addClass("btn-danger");
	                	}
					}
				})
			}
		}
	},
	document_type(frm){
	    frm.set_value("chosen_type", frm.doc.document_type)
	    if(frm.doc.document_type == "Delivery Note"){
	        frm.set_value("singkatan", "DN-")
	    }
	    else if(frm.doc.document_type == "Purchase Receipt"){
	        frm.set_value("singkatan", "PR-")
	    }
	    else if(frm.doc.document_type == "Stock Entry"){
	        frm.set_value("singkatan", "STE-")
	    }
	    else{
	        frm.set_value("singkatan", "")
	    }

	    if(frm.doc.chosen_type == "Stock Entry"){
			 frm.set_query("document_number", function() {
    			return {
    				query: "addons.custom_standard.custom_confirmation_document.get_stock_entry_for_confirmation_document",
    			};
    		});
		}
		else{
			frm.set_query("document_number", function() {
    			return {
    			    filters:{
    			        "docstatus": 0
    			    }
    			};
    		});
		}
		
	    frm.set_value("document_number", "")
        frm.set_value("items", [])
        frm.set_value("pr_items", [])
	        
	   
	},
	get_data(frm){
	   frm.set_value("items", [])
       frm.set_value("pr_items", [])
       frm.set_value("is_return", "")
       frm.set_value("tipe_stock", "")
       
	   if(frm.doc.document_type && frm.doc.document_number){
	   		if(frm.doc.document_type == "Delivery Note"){
	   			return frappe.call({
					method: 'addons.custom_method.get_document_detail',
					args: {
						"doctype":frm.doc.document_type,
						"docname":frm.doc.document_number
					},
					callback: function(r) {
					    frm.doc.items = []
						console.log(r.message)
						for(var baris_hasil in r.message){
	                       frm.doc.customer = r.message[baris_hasil][5]
	                       
	                       frm.doc.transporter = r.message[baris_hasil][7]
	                       frm.doc.driver = r.message[baris_hasil][8]
	                       frm.doc.lr_no = r.message[baris_hasil][9]
	                       frm.doc.vehicle_no = r.message[baris_hasil][10]
	                       frm.doc.transporter_name = r.message[baris_hasil][11]
	                       frm.doc.driver_name = r.message[baris_hasil][12]
	                       frm.doc.lr_date = r.message[baris_hasil][13]
	                       
	                       if(r.message[baris_hasil][6] == 1){
	                       		frm.doc.is_return = "Yes"
	                       		frm.doc.tipe_stock = "In"
								
	                       		var baris_baru = frm.add_child('pr_items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_terima = r.message[baris_hasil][4]
								baris_baru.qty_rencana_terima = r.message[baris_hasil][4]
								baris_baru.check_rencana_bongkar = 0
		                        
	                   		}
	                        else{
	                       		frm.doc.is_return = "No"
	                       		frm.doc.tipe_stock = "Out"
	                       		var baris_baru = frm.add_child('items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_muat = r.message[baris_hasil][4]
								baris_baru.qty_rencana_kirim = r.message[baris_hasil][4]
								baris_baru.check_rencana_kirim = 0
		                        
	                        }
	                    }
						frm.refresh_fields()
					}
				})
	   		}	
	   		else if(frm.doc.document_type == "Purchase Receipt"){
	   			return frappe.call({
					method: 'addons.custom_method.get_document_detail',
					args: {
						"doctype":frm.doc.document_type,
						"docname":frm.doc.document_number
					},
					callback: function(r) {
					    frm.doc.items = []
						console.log(r.message)
						for(var baris_hasil in r.message){
	                       frm.doc.supplier = r.message[baris_hasil][5]
	                       frm.doc.transporter_name = r.message[baris_hasil][7]
	                       frm.doc.lr_no = r.message[baris_hasil][8]
	                       frm.doc.lr_date = r.message[baris_hasil][9]

	                       if(r.message[baris_hasil][6] == 0){
	                       		frm.doc.is_return = "No"
	                       		frm.doc.tipe_stock = "In"
								
	                       		var baris_baru = frm.add_child('pr_items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_terima = r.message[baris_hasil][4]
								baris_baru.qty_rencana_terima = r.message[baris_hasil][4]
								baris_baru.check_rencana_bongkar = 0
		                        
	                   		}
	                        else{
	                       		frm.doc.is_return = "Yes"
	                       		frm.doc.tipe_stock = "Out"
	                       		var baris_baru = frm.add_child('items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_muat = r.message[baris_hasil][4]
								baris_baru.qty_rencana_kirim = r.message[baris_hasil][4]
								baris_baru.check_rencana_kirim = 0
		                        
	                        }
	                    }
						frm.refresh_fields()
					}
				})
	   		}
	   		else if(frm.doc.document_type == "Stock Entry"){
	   			return frappe.call({
					method: 'addons.custom_method.get_document_detail',
					args: {
						"doctype":frm.doc.document_type,
						"docname":frm.doc.document_number
					},
					callback: function(r) {
					    frm.doc.items = []
						console.log(r.message)
						for(var baris_hasil in r.message){
	                       if(r.message[baris_hasil][6] == "Material Receipt"){
	                       		frm.doc.is_return = "No"
	                       		frm.doc.tipe_stock = "In"
								
	                       		var baris_baru = frm.add_child('pr_items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_terima = r.message[baris_hasil][4]
								baris_baru.qty_rencana_terima = r.message[baris_hasil][4]
		                        baris_baru.check_rencana_bongkar = 0
	                   		}
	                        else{
	                       		frm.doc.is_return = "No"
	                       		frm.doc.tipe_stock = "Out"
	                       		var baris_baru = frm.add_child('items')
								baris_baru.item_code = r.message[baris_hasil][0]
								baris_baru.item_name = r.message[baris_hasil][1]
								baris_baru.sumber_document = r.message[baris_hasil][2]
								baris_baru.sumber_document_name = r.message[baris_hasil][3]
								baris_baru.qty_muat = r.message[baris_hasil][4]
								baris_baru.qty_rencana_kirim = r.message[baris_hasil][4]
								baris_baru.check_rencana_kirim = 0
		                        
	                        }
	                    }
						frm.refresh_fields()
					}
				})
	   		}
			
		}
	    
	}
		
})