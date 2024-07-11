frappe.ui.form.on('Item', {

	refresh: function(frm) {
		if(frm.doc.klasifikasi_barang == "NON WOVEN" && frm.doc.gramasi_ && frm.doc.lebar && frm.doc.index_kg){
			frm.doc.harga_barang = frm.doc.gramasi_ * frm.doc.lebar * frm.doc.index_kg / 1000
			frm.refresh_fields()
		}
	},
	klasifikasi_barang: function(frm) {
		if(frm.doc.klasifikasi_barang == "NON WOVEN" && frm.doc.gramasi_ && frm.doc.lebar && frm.doc.index_kg){
			frm.doc.harga_barang = frm.doc.gramasi_ * frm.doc.lebar * frm.doc.index_kg / 1000
			frm.refresh_fields()
		}
	},
	gramasi_: function(frm) {
		if(frm.doc.klasifikasi_barang == "NON WOVEN" && frm.doc.gramasi_ && frm.doc.lebar && frm.doc.index_kg){
			frm.doc.harga_barang = frm.doc.gramasi_ * frm.doc.lebar * frm.doc.index_kg / 1000
			frm.refresh_fields()
		}
	},
	lebar: function(frm) {
		if(frm.doc.klasifikasi_barang == "NON WOVEN" && frm.doc.gramasi_ && frm.doc.lebar && frm.doc.index_kg){
			frm.doc.harga_barang = frm.doc.gramasi_ * frm.doc.lebar * frm.doc.index_kg / 1000
			frm.refresh_fields()
		}
	},
	index_kg: function(frm) {
		if(frm.doc.klasifikasi_barang == "NON WOVEN" && frm.doc.gramasi_ && frm.doc.lebar && frm.doc.index_kg){
			frm.doc.harga_barang = frm.doc.gramasi_ * frm.doc.lebar * frm.doc.index_kg / 1000
			frm.refresh_fields()
		}
	},

	

});
