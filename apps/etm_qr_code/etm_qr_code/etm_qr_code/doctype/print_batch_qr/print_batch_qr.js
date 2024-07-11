// Copyright (c) 2022, DAS DEV and contributors
// For license information, please see license.txt

frappe.ui.form.on('Print Batch QR', {
	refresh: function (frm) {
		frm.add_custom_button(__('Download PDF'), function () {
			if (cur_frm.doc.__unsaved == 1) {
				frappe.msgprint({
					title: __('Tidak Dapat Mengunduh File'),
					indicator: 'red',
					message: __('Mohon simpan data terlebih dahulu untuk dapat mengunduh PDF QR Code')
				})
			} else {
				const URL = "/api/method/etm_qr_code.custom_print.print_format.download_pdf?doctype=Print Batch QR&name=Print Batch QR&format=Print Batch QR&no_letterhead=0&letterhead=Tanda Terima Faktur Asli&settings={}&_lang=en"
				window.open(URL, '_blank');
			}
		})

	},

	// End of hooks ------------------------
	pilih_data: function (frm) {
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Registration Packing ID",
			target: cur_frm,
			setters: {
				purchase_receipt: null,
				item: null
			},
			add_filters_group: 0,
			action(selections) {
				let latestData = frm.doc.list_registration_packing_id
				selections.forEach(data => {
					if (latestData == "" || latestData == undefined || latestData == null) {
						latestData += data
					} else {
						latestData += "\n" + data
					}
				})
				frm.set_value("list_registration_packing_id", latestData)
				frappe.show_alert({
					message: __(`${selections.length} Data Ditambahkan ke List Registration Packing ID`),
					indicator: 'green'
				}, 5)
				cur_dialog.hide()
			}
		})
	},

	ambil_data: function (frm) {
		let listRpiString = frm.doc.list_registration_packing_id
		if (listRpiString == "" || listRpiString == undefined || listRpiString == null) {
			frappe.msgprint({
				title: __('List Registration Packing ID Kosong'),
				indicator: 'red',
				message: __('Silahkan isi List Registration Packing ID untuk dapat melakukan ambil data.')
			})
			return
		}
		let listRPI = frm.doc.list_registration_packing_id.split("\n")
		cur_frm.events.get_list_data_for_child(listRPI, frm)
	},

	get_list_data_for_child: function (listRPI, frm) {
		frm.set_value("print_registration_packing_id", [])
		frappe.db.get_list('Registration Packing ID', {
			filters: {
				name: ["IN", listRPI],
			},
			fields: ["name", "item", "item_name", "conversion", "stock_uom", "uom_packing", "qr_code", "lot_number"],
			limit: 9999
		}).then(res => {
			let idDitemukan = []
			res.forEach(data => {
				idDitemukan.push(data['name'])
				let s = frm.add_child('print_registration_packing_id')
				s.id_packing = data['name']
				s.item = data['item']
				s.item_name = data['item_name']
				s.conversion = data['conversion']
				s.stock_uom = data['stock_uom']
				s.uom_packing = data['uom_packing']
				s.qr_code = data['qr_code']
				s.lot_number = data['lot_number']
			})
			cur_frm.refresh_fields()
			frappe.show_alert({
				message: __(`${res.length} Data Ditemukan`),
				indicator: 'green'
			}, 5)

			// Check ID tidak ditemukan
			let idTidakDitemukan = listRPI.filter(x => !idDitemukan.includes(x))
			let idTidakDitemukanString = "<ul>"
			idTidakDitemukan.forEach(data => {
				idTidakDitemukanString += "<li>" + data + "</li>"
			})
			idTidakDitemukanString += "</ul>"
			if (idTidakDitemukan.length > 0) {
				frappe.msgprint({
					title: __('Data Tidak Ditemukan'),
					indicator: 'red',
					message: __(`Terdapat ${idTidakDitemukan.length} Data Tidak Ditemukan:<br> ${idTidakDitemukanString}`)
				})
			}
		})
	}
});
