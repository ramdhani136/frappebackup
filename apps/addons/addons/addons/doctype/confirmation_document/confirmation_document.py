# Copyright (c) 2022, PT DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
class ConfirmationDocument(Document):

	def validate(self):
		installed = json.loads(frappe.db.get_global("installed_apps") or "[]")
		if "etm_qr_code" in installed:
			# Cek apakah kalau pake scan QR, itemsnya itu sudah pernah is_in / is_out sebelumnya
			self.check_ketersediaan_qr()
			self.set_list_qr_qty()

	def before_submit(self):
		installed = json.loads(frappe.db.get_global("installed_apps") or "[]")
		if "etm_qr_code" in installed:
			if self.document_type == "Stock Entry" or self.document_type == "Purchase Receipt":
				self.update_is_in_registration_packing_id()
			elif self.document_type == "Delivery Note":
				self.update_is_out_registration_packing_id()
			else:
				pass

	def before_insert(self):
		installed = json.loads(frappe.db.get_global("installed_apps") or "[]")
		if "etm_qr_code" in installed:
			for item in self.items:
				item.is_use_qr_code = frappe.get_value("Item", item.item_code, "is_use_qr_code")
			for item in self.pr_items:
				item.is_use_qr_code = frappe.get_value("Item", item.item_code, "is_use_qr_code")

	# End of hooks --------
	def set_list_qr_qty(self):
		for item in self.items:
			if item.qr_qty_rencana_kirim == None or item.qr_qty_rencana_kirim == "":
				pass
			else:
				list_qr = item.qr_qty_rencana_kirim.split("\n")
				if (len(list_qr) > 0):
					list_rpi = frappe.db.sql("""
						SELECT
							name, conversion, stock_uom
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					qty_rencana_kirim_qty = ""
					for rpi in list_rpi:
						qty_rencana_kirim_qty = "{}{} => {} {}\n".format(qty_rencana_kirim_qty,rpi.name,rpi.conversion,rpi.stock_uom)

					list_colly = frappe.db.sql("""
						SELECT
							COUNT(name) AS jumlah, conversion
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
						GROUP BY
							conversion
						ORDER BY
							conversion ASC
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					summary_colly = "Total Colly = "
					for rpi in list_colly:
						summary_colly = "{}{}/{}, ".format(summary_colly,rpi.jumlah,rpi.conversion)

					item.qr_qty_rencana_kirim_qty = "{}{}".format(qty_rencana_kirim_qty,summary_colly)
				else:
					pass

			if item.qr_qty_muat == None or item.qr_qty_muat == "":
				pass
			else:
				list_qr = item.qr_qty_muat.split("\n")
				if (len(list_qr) > 0):
					list_rpi = frappe.db.sql("""
						SELECT
							name, conversion, stock_uom
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					qr_qty_muat_qty = ""
					for rpi in list_rpi:
						qr_qty_muat_qty = "{}{} => {} {}\n".format(qr_qty_muat_qty,rpi.name,rpi.conversion,rpi.stock_uom)

					list_colly = frappe.db.sql("""
						SELECT
							COUNT(name) AS jumlah, conversion
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
						GROUP BY
							conversion
						ORDER BY
							conversion ASC
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					summary_colly = "Total Colly = "
					for rpi in list_colly:
						summary_colly = "{}{}/{}, ".format(summary_colly,rpi.jumlah,rpi.conversion)

					item.qr_qty_muat_qty = "{}{}".format(qr_qty_muat_qty,summary_colly)
				else:
					pass
		
		for item in self.pr_items:
			if item.qr_qty_rencana_terima == None or item.qr_qty_rencana_terima == "":
				pass
			else:
				list_qr = item.qr_qty_rencana_terima.split("\n")
				if (len(list_qr) > 0):
					list_rpi = frappe.db.sql("""
						SELECT
							name, conversion, stock_uom
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					qr_qty_rencana_terima_qty = ""
					for rpi in list_rpi:
						qr_qty_rencana_terima_qty = "{}{} => {} {}\n".format(qr_qty_rencana_terima_qty,rpi.name,rpi.conversion,rpi.stock_uom)

					list_colly = frappe.db.sql("""
						SELECT
							COUNT(name) AS jumlah, conversion
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
						GROUP BY
							conversion
						ORDER BY
							conversion ASC
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					summary_colly = "Total Colly = "
					for rpi in list_colly:
						summary_colly = "{}{}/{}, ".format(summary_colly,rpi.jumlah,rpi.conversion)

					item.qr_qty_rencana_terima_qty = "{}{}".format(qr_qty_rencana_terima_qty,summary_colly)
				else:
					pass

			if item.qr_qty_terima == None or item.qr_qty_terima == "":
				pass
			else:
				list_qr = item.qr_qty_terima.split("\n")
				if (len(list_qr) > 0):
					list_rpi = frappe.db.sql("""
						SELECT
							name, conversion, stock_uom
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					qr_qty_terima_qty = ""
					for rpi in list_rpi:
						qr_qty_terima_qty = "{}{} => {} {}\n".format(qr_qty_terima_qty,rpi.name,rpi.conversion,rpi.stock_uom)

					list_colly = frappe.db.sql("""
						SELECT
							COUNT(name) AS jumlah, conversion
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
						GROUP BY
							conversion
						ORDER BY
							conversion ASC
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					summary_colly = "Total Colly = "
					for rpi in list_colly:
						summary_colly = "{}{}/{}, ".format(summary_colly,rpi.jumlah,rpi.conversion)

					item.qr_qty_terima_qty = "{}{}".format(qr_qty_terima_qty,summary_colly)
				else:
					pass


	def update_is_in_registration_packing_id(self):
		for item in self.items:
			if item.is_use_qr_code == 1:
				if item.qr_qty_muat == None or item.qr_qty_muat == "":
					pass
				else:
					list_qr = item.qr_qty_muat.split("\n")
					if len(list_qr) > 0:
						# Update Data
						frappe.db.sql("""
							UPDATE `tabRegistration Packing ID`
							SET
								is_in = 1,
								is_in_name = %(name)s
							WHERE
								name IN %(list_qr)s
						""", {
							"list_qr": list_qr,
							"name": self.name
						})
					else:
						pass
			else:
				pass
		for item in self.pr_items:
			if item.is_use_qr_code == 1:
				if item.qr_qty_terima == None or item.qr_qty_terima == "":
					pass
				else:
					list_qr = item.qr_qty_terima.split("\n")
					if len(list_qr) > 0:
						# Update Data
						frappe.db.sql("""
							UPDATE `tabRegistration Packing ID`
							SET
								is_in = 1,
								is_in_name = %(name)s
							WHERE
								name IN %(list_qr)s
						""", {
							"list_qr": list_qr,
							"name": self.name
						})
					else:
						pass
			else:
				pass
		
		# Commit
		frappe.db.commit()

	def update_is_out_registration_packing_id(self):
		self.check_ketersediaan_qr_sebelum_submit()
		for item in self.items:
			if item.is_use_qr_code == 1:
				if item.qr_qty_muat == None or item.qr_qty_muat == "":
					pass
				else:
					list_qr = item.qr_qty_muat.split("\n")
					if len(list_qr) > 0:
						# Update Data
						frappe.db.sql("""
							UPDATE `tabRegistration Packing ID`
							SET
								is_out = 1,
								is_out_name = %(name)s
							WHERE
								name IN %(list_qr)s
						""", {
							"list_qr": list_qr,
							"name": self.name
						})
					else:
						pass
			else:
				pass
		for item in self.pr_items:
			if item.is_use_qr_code == 1:
				if item.qr_qty_terima == None or item.qr_qty_terima == "":
					pass
				else:
					list_qr = item.qr_qty_terima.split("\n")
					if len(list_qr) > 0:
						# Update Data
						frappe.db.sql("""
							UPDATE `tabRegistration Packing ID`
							SET
								is_out = 1,
								is_out_name = %(name)s
							WHERE
								name IN %(list_qr)s
						""", {
							"list_qr": list_qr,
							"name": self.name
						})
					else:
						pass
			else:
				pass
		
		# Commit
		frappe.db.commit()

	def check_ketersediaan_qr_sebelum_submit(self):
		# ambil list QR code nya
		list_qr = []
		if len(self.items) > 0:
			for item in self.items:
				if item.is_use_qr_code == 1:
					if item.qr_qty_muat == None or item.qr_qty_muat == "":
						pass
					else:
						for qr in item.qr_qty_muat.split("\n"):
							if qr != "":
								list_qr.append(qr)
							else:
								pass
				else:
					pass
		else:
			# Kalau PR pass karena input check stocknya manual
			if self.document_type == "Purchase Receipt":
				pass
			else:
				for item in self.pr_items:
					if item.is_use_qr_code == 1:
						if item.qr_qty_terima == None or item.qr_qty_terima == "":
							pass
						else:
							for qr in item.qr_qty_terima.split("\n"):
								if qr != "":
									list_qr.append(qr)
								else:
									pass
					else:
						pass
		
		# Kalau list_qr nya ada isinya maka check
		if len(list_qr)> 0:
			list_rpi = frappe.db.sql("""
				SELECT
					name, is_in, is_out
				FROM 
					`tabRegistration Packing ID`
				WHERE
					name IN %(list_qr)s
			""", {
				"list_qr": list_qr
			}, 
				as_dict = True
			)
			list_rpi_yang_belum_is_in = []
			list_rpi_yang_sudah_is_out = []
			for rpi in list_rpi:
				if rpi.is_in == 0:
					list_rpi_yang_belum_is_in.append(rpi.name)
				else:
					pass

				if rpi.is_out == 1:
					list_rpi_yang_sudah_is_out.append(rpi.name)
				else:
					pass

			if len(list_rpi_yang_belum_is_in) > 0:
				frappe.throw("Registration Packing ID: {}, belum pernah dimasukkan ke system.".format(list_rpi_not_available))
			elif len(list_rpi_yang_sudah_is_out) > 0:
				frappe.throw("Registration Packing ID: {}, sudah pernah dikeluarkan dari system.".format(list_rpi_not_available))
			else:
				pass
		else:
			pass

	def check_data_qr_inputted(self,item,list_qr_inputted,list_qr_rencana):
		# Check apakah list qr yang di input kosong
		# Jika rencana nya 0 maka yang di input juga boleh 0
		if len(list_qr_rencana) > 0 and len(list_qr_inputted) == 0:
			frappe.throw("Item: {} belum di scan QR nya.\nSilahkan scan menggunakan aplikasi.".format(item.item_code))
		else:
			pass
		# Pengecekan QR Terima / Kirim harus QR yang terdaftar di QR Rencana
		# Kalau PR di bypass
		if self.document_type == "Purchase Receipt":
			pass
		else:
			list_qr_yang_tidak_ada_di_rencana = []
			for qr in list_qr_inputted:
				if qr in list_qr_rencana:
					pass
				else:
					list_qr_yang_tidak_ada_di_rencana.append(qr)

			if len(list_qr_yang_tidak_ada_di_rencana) > 0:
				frappe.throw("Item: {} QR Code nya tidak dapat di proses oleh system karena tidak di daftarkan saat Scan QR Rencana.\n{}".format(item.item_code, list_qr_yang_tidak_ada_di_rencana))
			else:
				pass

	def check_ketersediaan_qr(self):
		if self.document_type == "Stock Entry" or self.document_type == "Purchase Receipt":
			# ambil list QR code nya
			list_qr = []
			if len(self.items) > 0:
				for item in self.items:
					if item.check_rencana_kirim == 1 and item.checking_stock == 1 and item.check_qty_muat == 0 and item.check_konfirmasi == 0:
						if item.qr_qty_rencana_kirim == None or item.qr_qty_rencana_kirim == "":
							pass
						else:
							for qr in item.qr_qty_rencana_kirim.split("\n"):
								if qr != "":
									list_qr.append(qr)
								else:
									pass
					elif item.check_rencana_kirim == 1 and item.checking_stock == 1 and item.check_qty_muat == 1 and item.check_konfirmasi == 0:
						list_qr_inputted = []
						list_qr_rencana = []
						if item.qr_qty_muat == None or item.qr_qty_muat == "":
							pass
						else:
							for qr in item.qr_qty_muat.split("\n"):
								if qr != "":
									list_qr.append(qr)
									list_qr_inputted.append(qr)
								else:
									pass
						if item.qr_qty_rencana_kirim == None or item.qr_qty_rencana_kirim == "":
							pass
						else:
							for qr in item.qr_qty_rencana_kirim.split("\n"):
								if qr != "":
									list_qr_rencana.append(qr)
								else:
									pass
						self.check_data_qr_inputted(item,list_qr_inputted,list_qr_rencana)
					else:
						pass
			else:
				for item in self.pr_items:
					if item.check_rencana_bongkar == 1 and item.checking_stock == 1 and item.check_qty_terima == 0 and item.check_konfirmasi == 0:
						if item.qr_qty_rencana_terima == None or item.qr_qty_rencana_terima == "":
							pass
						else:
							for qr in item.qr_qty_rencana_terima.split("\n"):
								if qr != "":
									list_qr.append(qr)
								else:
									pass
					elif item.check_rencana_bongkar == 1 and item.checking_stock == 1 and item.check_qty_terima == 1 and item.check_konfirmasi == 0:
						list_qr_inputted = []
						list_qr_rencana = []
						if item.qr_qty_terima == None or item.qr_qty_terima == "":
							pass
						else:
							for qr in item.qr_qty_terima.split("\n"):
								if qr != "":
									list_qr.append(qr)
									list_qr_inputted.append(qr)
								else:
									pass
						if item.qr_qty_rencana_terima == None or item.qr_qty_rencana_terima == "":
							pass
						else:
							for qr in item.qr_qty_rencana_terima.split("\n"):
								if qr != "":
									list_qr_rencana.append(qr)
								else:
									pass
						self.check_data_qr_inputted(item,list_qr_inputted,list_qr_rencana)
					else:
						pass

			# Kalau list_qr nya ada isinya maka check
			if self.document_type == "Purchase Receipt":
				pass
			else:
				if len(list_qr)> 0:
					list_rpi = frappe.db.sql("""
						SELECT
							name, is_in, is_out
						FROM 
							`tabRegistration Packing ID`
						WHERE
							name IN %(list_qr)s
					""", {
						"list_qr": list_qr
					}, 
						as_dict = True
					)
					list_rpi_not_available = []
					for rpi in list_rpi:
						if rpi.is_in == 1:
							list_rpi_not_available.append(rpi.name)
						else:
							pass

					if len(list_rpi_not_available) > 0:
						frappe.throw("Registration Packing ID: {}, sudah pernah dimasukkan ke system.".format(list_rpi_not_available))
					else:
						pass
				else:
					pass
		elif self.document_type == "Delivery Note":
			# ambil list QR code nya
			list_qr = []
			if len(self.items) > 0:
				for item in self.items:
					if item.is_use_qr_code == 1:
						if item.check_rencana_kirim == 1 and item.checking_stock == 1 and item.check_qty_muat == 0 and item.check_konfirmasi == 0:
							#skip qr if kosong
							if item.qr_qty_rencana_kirim == None or item.qr_qty_rencana_kirim == "":
								pass
							else:
								for qr in item.qr_qty_rencana_kirim.split("\n"):
									if qr != "":
										list_qr.append(qr)
									else:
										pass
						elif item.check_rencana_kirim == 1 and item.checking_stock == 1 and item.check_qty_muat == 1 and item.check_konfirmasi == 0:
							#skip qr if kosong
							if item.qr_qty_muat == None or item.qr_qty_muat == "":
								pass
							else:
								for qr in item.qr_qty_muat.split("\n"):
									if qr != "":
										list_qr.append(qr)
									else:
										pass
						else:
							pass
					else:
						pass
			else:
				for item in self.pr_items:
					if item.is_use_qr_code == 1:
						if item.check_rencana_bongkar == 1 and item.checking_stock == 1 and item.check_qty_terima == 0 and item.check_konfirmasi == 0:
							if item.qr_qty_rencana_terima == None or item.qr_qty_rencana_terima == "":
								pass
							else:
								for qr in item.qr_qty_rencana_terima.split("\n"):
									if qr != "":
										list_qr.append(qr)
									else:
										pass
						elif item.check_rencana_bongkar == 1 and item.checking_stock == 1 and item.check_qty_terima == 1 and item.check_konfirmasi == 0:
							if item.qr_qty_terima == None or item.qr_qty_terima == "":
								pass
							else:
								for qr in item.qr_qty_terima.split("\n"):
									if qr != "":
										list_qr.append(qr)
									else:
										pass
						else:
							pass
					else:
						pass
			
			# Kalau list_qr nya ada isinya maka check
			if len(list_qr)> 0:
				list_rpi = frappe.db.sql("""
					SELECT
						name, is_in, is_out
					FROM 
						`tabRegistration Packing ID`
					WHERE
						name IN %(list_qr)s
				""", {
					"list_qr": list_qr
				}, 
					as_dict = True
				)
				list_rpi_yang_belum_is_in = []
				list_rpi_yang_sudah_is_out = []
				for rpi in list_rpi:
					if rpi.is_in == 0:
						list_rpi_yang_belum_is_in.append(rpi.name)
					else:
						pass

					if rpi.is_out == 1:
						list_rpi_yang_sudah_is_out.append(rpi.name)
					else:
						pass

				if len(list_rpi_yang_belum_is_in) > 0:
					frappe.throw("Registration Packing ID: {}, belum pernah dimasukkan ke system.".format(list_rpi_yang_belum_is_in))
				elif len(list_rpi_yang_sudah_is_out) > 0:
					frappe.throw("Registration Packing ID: {}, sudah pernah dikeluarkan dari system.".format(list_rpi_yang_sudah_is_out))
				else:
					pass
			else:
				pass
		else:
			pass

