frappe.ui.form.on('Price List Generator', {
	onload(frm) {
    	if(frm.doc.parent_item_group){
			frappe.db.get_value("Item Group", {"name": frm.doc.parent_item_group}, "is_group", function(value) {
	            if(value["is_group"] == 0){
	            	frm.doc.item_group = frm.doc.parent_item_group
	            	frm.refresh_fields()
	            	frm.set_df_property("item_group", "hidden", 1);
	            }
	            else{
	            	if(!frm.doc.item_group){
	            		frm.doc.item_group = ""
	            		frm.refresh_fields()
	            	}
	            	frm.set_df_property("item_group", "hidden", 0);
	            }
	        });
	        frm.set_query("item_group", function() {
				return {
				    query:"addons.addons.doctype.price_list_generator.price_list_generator.query_item_group",
				    filters:{
				        "field_parent_item_group": cur_frm.doc.parent_item_group
				    }
				};
			});
		}
	},
	price_list(frm){
	    if(frm.doc.price_list){
            frappe.db.get_value("Price List", {"name": frm.doc.price_list}, ["selling","buying"], function(value) {
                if(value.buying == 1){
                    frm.doc.tipe_price_list = "Buying"
                    frm.refresh_fields()
                }
                else if(value.selling == 1){
                    frm.doc.tipe_price_list = "Selling"
                    frm.refresh_fields()
                }
            });
	    }
	    if(frm.doc.filter_by == "Item Code"){
	    	for(var row in frm.doc.item_code_table){
		    	var item_code = frm.doc.item_code_table[row] 
				if(item_code.item_code){
					frappe.call({
						method: 'addons.addons.doctype.price_list_generator.price_list_generator.get_history',
						args: {
							"filter_by":frm.doc.filter_by,
							"item_code":item_code.item_code,
							"price_list":frm.doc.price_list || ""
						},
						callback: function(r) {
							if(r){
								item_code.history = r["message"]
								frm.refresh_fields()
							}					
						}
					})
				}
		    }
	    }
	},
	parent_item_group(frm){
		if(frm.doc.parent_item_group){
			frappe.db.get_value("Item Group", {"name": frm.doc.parent_item_group}, "is_group", function(value) {
	            if(value["is_group"] == 0){
	            	console.log(frm.doc.parent_item_group)
	            	frm.doc.item_group = frm.doc.parent_item_group
	            	frm.refresh_fields()
	            	frm.set_df_property("item_group", "hidden", 1);
	            }
	            else{
	            	frm.doc.item_group = ""
	            	frm.refresh_fields()
	            	frm.set_df_property("item_group", "hidden", 0);
	            }
	        });
	        frm.set_query("item_group", function() {
				return {
				    query:"addons.addons.doctype.price_list_generator.price_list_generator.query_item_group",
				    filters:{
				        "field_parent_item_group": cur_frm.doc.parent_item_group
				    }
				};
			});
			
			frappe.call({
				method: 'addons.addons.doctype.price_list_generator.price_list_generator.get_history',
				args: {
					"filter_by":frm.doc.filter_by,
					"item_code":frm.doc.parent_item_group,
					"price_list":frm.doc.price_list || ""
				},
				callback: function(r) {
					if(r){
						frm.doc.history_item_group = r["message"]
						frm.refresh_fields()
					}					
				}
			})
		}
	},
	item_group(frm){
		if(frm.doc.item_group){
			frappe.call({
				method: 'addons.addons.doctype.price_list_generator.price_list_generator.get_history',
				args: {
					"filter_by":frm.doc.filter_by,
					"item_code":frm.doc.item_group,
					"price_list":frm.doc.price_list || ""
				},
				callback: function(r) {
					if(r){
						frm.doc.history_item_group = r["message"]
						frm.refresh_fields()
					}					
				}
			})
		}
	}
});

frappe.ui.form.on('Price List Generator Item', {
	item_code(frm,cdt,cdn){
		var item_code = locals[cdt][cdn]
		if(item_code.item_code){
			frappe.call({
				method: 'addons.addons.doctype.price_list_generator.price_list_generator.get_history',
				args: {
					"filter_by":frm.doc.filter_by,
					"item_code":item_code.item_code,
					"price_list":frm.doc.price_list || ""
				},
				callback: function(r) {
					if(r){
						item_code.history = r["message"]
						frm.refresh_fields()
					}					
				}
			})
		}
	}
});	
cur_frm.add_fetch('item_code',  'item_name',  'item_name');
cur_frm.add_fetch('item_code',  'stock_uom',  'filter_uom');
