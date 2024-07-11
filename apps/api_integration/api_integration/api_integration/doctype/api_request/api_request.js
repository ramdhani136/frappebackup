// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

var and_filters = ""

frappe.ui.form.on('API Request', {
	refresh: function(frm) {
		frm.events.lock_event()
		document.querySelectorAll("[data-fieldname='test_api']")[1].classList.add("btn-primary");
		document.querySelectorAll("[data-fieldname='description']")[1].style.height = "50px"
	},
	lock_event:function(){
		if(cur_frm.doc.lock == 1){
			if (cur_frm.doc.description)
			{cur_frm.set_intro(cur_frm.doc.description);}
			cur_frm.fields.forEach(function(l){ 
				if (l.df.fieldname != "response"){ cur_frm.set_df_property(l.df.fieldname, "read_only", 1); }})
		}else if (cur_frm.doc.lock==0){
			cur_frm.set_intro("");
			cur_frm.fields.forEach(function(l){ cur_frm.set_df_property(l.df.fieldname, "read_only", 0); })
		}
		cur_frm.set_df_property("lock","read_only",0)
	},
	lock:function(frm){
		frm.events.lock_event()
	},
	doc_action:function(frm){
		if (frm.doc.doc_action == "frappe.get_doc"){
			if (frm.doc.and_filters != "and_filters",'{ "name": ["=", "<name>"] }'){
				and_filters = frm.doc.and_filters}
			frm.set_value("and_filters",'{ "name": ["=", "<name>"] }')
		}
		// else{
		// 	frm.set_value("and_filters",and_filters)
		// }
	}
});
