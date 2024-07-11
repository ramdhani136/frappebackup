# from __future__ import unicode_literals
# import frappe
# import frappe.utils
# from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html

# @frappe.whitelist()
# def update_dn_qty_muat(doc,doctype,qty):
# 	frappe.db.sql("""
# 		UPDATE `tab{}` 
# 		SET qty = {} 
# 		WHERE name = "{}" 
# 	""".format(doctype,qty,doc))

# @frappe.whitelist()
# def on_trash(doc,method):
# 	frappe.db.sql(""" UPDATE `tab{}` SET confirmation_document = "" WHERE confirmation_document = "{}" and name = "{}" """.format(doc.document_type,doc.name,doc.document_number))

# @frappe.whitelist()
# def on_cancel(doc, method):
# 	# if doc.chosen_type != "Delivery Note":
# 	# 	document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
# 	# 	# # document_asli.workflow_state = "Cancelled"
# 	# 	document_asli.cancel()
# 	pass
	
# @frappe.whitelist()
# def onload(doc, method):
# 	if doc.tipe_stock == "Out":
# 		check_pending = 1
# 		check_rencana_kirim = 1
# 		check_stock = 1
# 		check_muat = 1
# 		check_validation = 1
		
# 		for baris in doc.items:
# 			if not baris.check_rencana_kirim:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_rencana_kirim = 0
# 			if not baris.check_qty_muat:
# 				check_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_muat = 0

# 		if check_pending == 0:
# 			doc.workflow_state = "Pending"
# 		elif check_rencana_kirim == 0:
# 			doc.workflow_state = "Persiapan Rencana Kirim"
# 		elif check_stock == 0:
# 			doc.workflow_state = "Checker Stock"
# 		elif check_muat == 0:
# 			doc.workflow_state = "Checker Muat"
# 		elif check_muat == 1:
# 			doc.workflow_state = "Confirmation"

# 	elif doc.tipe_stock == "In":
# 		check_pending = 1
# 		check_bongkar = 1
# 		checking_stock = 1
# 		check_terima = 1
# 		check_review = 1
# 		for baris in doc.pr_items:
# 			if not baris.check_rencana_bongkar:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_bongkar = 0
# 			if not baris.check_qty_terima:
# 				checking_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_review = 0

# 		if check_pending == 0:
# 			doc.workflow_state = "Pending"
# 		elif check_bongkar == 0:
# 			doc.workflow_state = "Persiapan Bongkar"
# 		elif checking_stock == 0:
# 			doc.workflow_state = "Checker Stock Terima"
# 		elif check_terima == 0:
# 			doc.workflow_state = "Persiapan Terima"
# 		elif check_terima == 1:
# 			doc.workflow_state = "Confirmation"
	
# 	doc.db_update()


# @frappe.whitelist()
# def before_submit(doc, method):
# 	if doc.tipe_stock == "Out":
# 		check_pending = 1
# 		check_rencana_kirim = 1
# 		check_stock = 1
# 		check_muat = 1
# 		check_validation = 1
# 		for baris in doc.items:
# 			if not baris.check_rencana_kirim:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_rencana_kirim = 0
# 			if not baris.check_qty_muat:
# 				check_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_muat = 0

# 		if check_pending == 0 or check_rencana_kirim == 0 or check_stock == 0 or check_muat == 0 or check_validation == 0:
# 			frappe.throw("Document tidak bisa tersubmit jika ada centangan yang belum selesai.")
	
# 	elif doc.tipe_stock == "In":
# 		check_pending = 1
# 		check_bongkar = 1
# 		check_checking_stock = 1
# 		check_terima = 1
# 		check_review = 1
# 		for baris in doc.pr_items:
# 			if not baris.check_rencana_bongkar:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_bongkar = 0
# 			if not baris.check_qty_terima:
# 				check_checking_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_review = 0

# 		if check_pending == 0 or check_bongkar == 0 or check_checking_stock == 0 or check_terima == 0 or check_review == 0:
# 			frappe.throw("Document tidak bisa tersubmit jika ada centangan yang belum selesai.")
		

# @frappe.whitelist()
# def validate(doc, method):
# 	document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
# 	document_asli.confirmation_document = doc.name
# 	document_asli.db_update()

# 	if doc.tipe_stock == "Out":
# 		check_pending = 1
# 		check_rencana_kirim = 1
# 		check_stock = 1
# 		check_muat = 1
# 		check_validation = 1
# 		check_batal_kirim = 0
		
# 		for baris in doc.items:
# 			if not baris.check_rencana_kirim:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_rencana_kirim = 0
# 			if not baris.check_qty_muat:
# 				check_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_muat = 0

# 			if baris.batal_kirim:
# 				# frappe.msgprint("12414234")
# 				if doc.chosen_type == "Delivery Note":
# 					frappe.db.sql("""
# 						UPDATE `tabDelivery Note` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name = "{}" 
# 					""".format(doc.document_number))

# 					frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))

# 					doctype = "Delivery Note Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, batal_kirim = 1
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_muat,baris.sumber_document))

# 					dn = frappe.get_doc("Delivery Note",doc.document_number)
# 					for i in dn.items:
# 						i.amount = i.qty * i.rate

# 					dn.flags.ignore_permission = True
# 					dn.save()
# 					# frappe.msgprint("State menjadi Checker Muat. Delivery Note qty terupdate Tes.")
# 			else:
# 				# frappe.msgprint("5555")
# 				if doc.chosen_type == "Delivery Note":
# 					frappe.db.sql("""
# 						UPDATE `tabDelivery Note` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name = "{}" 
# 					""".format(doc.document_number))

# 					frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))

# 					doctype = "Delivery Note Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, batal_kirim = 0
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_muat,baris.sumber_document))

# 					dn = frappe.get_doc("Delivery Note",doc.document_number)
# 					for i in dn.items:
# 						i.amount = i.qty * i.rate

# 					dn.flags.ignore_permission = True
# 					dn.save()
# 					# frappe.msgprint("State menjadi Checker Muat. Delivery Note qty terupdate Tes.")

# 		if check_pending == 0:
# 			doc.workflow_state = "Pending"
# 		elif check_rencana_kirim == 0:
# 			doc.workflow_state = "Persiapan Rencana Kirim"
# 			if doc.chosen_type == "Delivery Note":
# 				frappe.db.sql("""
# 					UPDATE `tabDelivery Note` 
# 					SET workflow_state = "Pending"
# 					WHERE name = "{}" 
# 				""".format(doc.document_number))

# 				frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "Pending"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))
# 		elif check_stock == 0:
# 			doc.workflow_state = "Checker Stock"
# 			if doc.chosen_type == "Delivery Note":
# 				frappe.db.sql("""
# 					UPDATE `tabDelivery Note` 
# 					SET workflow_state = "In Confirmation Doc"
# 					WHERE name = "{}" 
# 				""".format(doc.document_number))

# 				frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))

# 				for baris in doc.items:
# 					doctype = "Delivery Note Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, keterangan_check = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_rencana_kirim,baris.keterangan_checking_stock,baris.sumber_document))

# 				dn = frappe.get_doc("Delivery Note",doc.document_number)
# 				for i in dn.items:
# 					i.amount = i.qty * i.rate

# 				dn.flags.ignore_permission = True
# 				dn.save()
# 				frappe.msgprint("State menjadi Checker Stock. Delivery Note qty terupdate.")

# 			elif doc.chosen_type == "Purchase Receipt":
# 				for baris in doc.items:
# 					doctype = "Purchase Receipt Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {} * 1, received_qty = {} * 1, keterangan_check = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_rencana_kirim,baris.qty_rencana_kirim,baris.keterangan_checking_stock,baris.sumber_document))
# 				frappe.msgprint("State menjadi Checker Stock. Purchase Receipt qty terupdate.")

# 			elif doc.chosen_type == "Stock Entry":
# 				for baris in doc.items:
# 					doctype = "Stock Entry Detail"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_rencana_kirim,baris.sumber_document))
# 				frappe.msgprint("State menjadi Checker Stock. Stock Entry qty terupdate.")
# 		elif check_muat == 0:
# 			if doc.chosen_type == "Delivery Note":
# 				frappe.db.sql("""
# 					UPDATE `tabDelivery Note` 
# 					SET workflow_state = "In Confirmation Doc"
# 					WHERE name = "{}" 
# 				""".format(doc.document_number))

# 				frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "In Confirmation Doc"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))
					
# 				for baris in doc.items:
# 					doctype = "Delivery Note Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, keterangan_muat = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_muat,baris.keterangan_muat,baris.sumber_document))

# 				dn = frappe.get_doc("Delivery Note",doc.document_number)
# 				for i in dn.items:
# 					i.amount = i.qty * i.rate

# 				dn.flags.ignore_permission = True
# 				dn.save()
# 				frappe.msgprint("State menjadi Checker Muat. Delivery Note qty terupdate.")

# 			elif doc.chosen_type == "Purchase Receipt":
# 				for baris in doc.items:
# 					doctype = "Purchase Receipt Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {} * 1, received_qty = {} * 1, keterangan_muat = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_muat,baris.qty_muat,baris.keterangan_muat,baris.sumber_document))
# 				frappe.msgprint("State menjadi Checker Muat. Purchase Receipt qty terupdate.")

# 			elif doc.chosen_type == "Stock Entry":
# 				for baris in doc.items:
# 					doctype = "Stock Entry Detail"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_muat,baris.sumber_document))
# 				frappe.msgprint("State menjadi Checker Muat. Stock Entry qty terupdate.")
# 			doc.workflow_state = "Checker Muat"
# 		# elif check_validation == 0:
# 		# 	if doc.chosen_type == "Delivery Note":
# 		# 		frappe.db.sql("""
# 		# 			UPDATE `tabDelivery Note` 
# 		# 			SET workflow_state = "In Confirmation Doc"
# 		# 			WHERE name = "{}" 
# 		# 		""".format(doc.document_number))

# 		# 		frappe.db.sql("""
# 		# 				UPDATE `tabDelivery Trip` 
# 		# 				SET workflow_state = "In Confirmation Doc"
# 		# 				WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 		# 			""".format(doc.document_number))

# 		# 	# frappe.db.sql(""" UPDATE `tab{}` SET workflow_state = "{}" WHERE name = "{}" """.format(doc.chosen_type,"Print DN",doc.document_number))
# 		# 	doc.workflow_state = "Validation"
# 		elif check_muat == 1:
# 			document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
# 			if doc.document_type == "Delivery Note":
# 				document_asli.workflow_state = "Print DN"
# 				document_asli.db_update()
# 				frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "Print DN"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi Print DN.".format(doc.chosen_type))

# 			elif doc.document_type == "Purchase Receipt":
# 				document_asli.workflow_state = "In Purchasing"
# 				document_asli.db_update()
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi In Purchasing.".format(doc.chosen_type))
# 			else:
# 				# document_asli.workflow_state = "Pending"
# 				# document_asli.db_update()
# 				# document_asli.submit()
# 				# document_asli.workflow_state = "Submitted"
# 				# doc.submit()
# 				# frappe.msgprint("State menjadi Confirmation. {} selesai tersubmit.".format(doc.chosen_type))
# 				document_asli.workflow_state = "In DIC"
# 				document_asli.db_update()
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi In DIC.".format(doc.chosen_type))


# 	elif doc.tipe_stock == "In":
# 		check_pending = 1
# 		check_bongkar = 1
# 		check_checking_stock = 1
# 		check_terima = 1
# 		check_review = 1
# 		for baris in doc.pr_items:
# 			if not baris.check_rencana_bongkar:
# 				check_pending = 0
# 			if not baris.checking_stock:
# 				check_bongkar = 0
# 			if not baris.check_qty_terima:
# 				check_checking_stock = 0
# 			if not baris.check_konfirmasi:
# 				check_terima = 0

# 		if check_pending == 0:
# 			doc.workflow_state = "Pending"
# 		elif check_bongkar == 0:
# 			doc.workflow_state = "Persiapan Bongkar"
# 		elif check_checking_stock == 0:
# 			doc.workflow_state = "Checker Stock Terima"

# 			if doc.chosen_type == "Delivery Note":
# 				for baris in doc.items:
# 					doctype = "Delivery Note Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {} * 1, keterangan_check = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_rencana_terima,baris.keterangan_checking_stock,baris.sumber_document))
# 				dn = frappe.get_doc("Delivery Note",doc.document_number)
# 				for i in dn.items:
# 					i.amount = i.qty * i.rate

# 				dn.flags.ignore_permission = True
# 				dn.save()
# 				frappe.msgprint("State menjadi Checker Stock Terima. Delivery Note qty terupdate.")

# 			elif doc.chosen_type == "Purchase Receipt":
# 				for baris in doc.pr_items:
# 					doctype = "Purchase Receipt Item"
# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, received_qty = {}, keterangan_check = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_rencana_terima,baris.qty_rencana_terima,baris.keterangan_checking_stock,baris.sumber_document))
# 				frappe.msgprint("State menjadi Checker Stock Terima. Purchase Receipt qty terupdate.")

# 		elif check_terima == 0:
# 			doc.workflow_state = "Persiapan Terima"

# 			if doc.chosen_type == "Delivery Note":
# 				for baris in doc.pr_items:
# 					doctype = doc.chosen_type
# 					if doc.chosen_type == "Delivery Note":
# 						doctype = "Delivery Note Item"

# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {} * 1, keterangan_muat = "{}" 
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_terima,baris.keterangan_terima,baris.sumber_document))
# 				dn = frappe.get_doc("Delivery Note",doc.document_number)
# 				for i in dn.items:
# 					i.amount = i.qty * i.rate

# 				dn.flags.ignore_permission = True
# 				dn.save()
# 				frappe.msgprint("State menjadi Persiapan Terima. Delivery Note qty terupdate.")

# 			elif doc.chosen_type == "Purchase Receipt":
# 				for baris in doc.pr_items:
# 					doctype = doc.chosen_type
# 					if doc.chosen_type == "Purchase Receipt":
# 						doctype = "Purchase Receipt Item"

# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}, received_qty = {}, keterangan_muat = "{}"
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_terima,baris.qty_terima,baris.keterangan_terima,baris.sumber_document))
# 				frappe.msgprint("State menjadi Persiapan Terima. Purchase Receipt qty terupdate.")

# 			elif doc.chosen_type == "Stock Entry":
# 				for baris in doc.pr_items:
# 					doctype = doc.chosen_type
# 					if doc.chosen_type == "Stock Entry":
# 						doctype = "Stock Entry Detail"

# 					frappe.db.sql("""
# 						UPDATE `tab{}` 
# 						SET qty = {}
# 						WHERE name = "{}" 
# 					""".format(doctype,baris.qty_terima,baris.sumber_document))
# 				frappe.msgprint("State menjadi Persiapan Terima. Stock Entry qty terupdate.")

# 		# elif check_review == 0:
# 		# 	doc.workflow_state = "Waiting Review"
			
# 		elif check_terima == 1:
# 			ddocument_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
# 			if doc.document_type == "Delivery Note":
# 				document_asli.workflow_state = "Print DN"
# 				document_asli.db_update()
# 				frappe.db.sql("""
# 						UPDATE `tabDelivery Trip` 
# 						SET workflow_state = "Print DN"
# 						WHERE name IN (Select parent From `tabDelivery Stop` Where delivery_note = "{}") 
# 					""".format(doc.document_number))
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi Print DN.".format(doc.chosen_type))
# 			elif doc.document_type == "Purchase Receipt":
# 				document_asli.workflow_state = "In Purchasing"
# 				document_asli.db_update()
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi In Purchasing.".format(doc.chosen_type))
# 			else:
# 				# document_asli.workflow_state = "Pending"
# 				# document_asli.db_update()
# 				# document_asli.submit()
# 				# document_asli.workflow_state = "Submitted"
# 				# doc.submit()
# 				# frappe.msgprint("State menjadi Confirmation. {} selesai tersubmit.".format(doc.chosen_type))
# 				document_asli.workflow_state = "In DIC"
# 				document_asli.db_update()
# 				doc.submit()
# 				frappe.msgprint("State menjadi Confirmation. {} menjadi In DIC.".format(doc.chosen_type))

# 	doc.db_update()
# 	# elif doc.chosen_type == "Stock Entry":
# 	# 	check_pending = 1
# 	# 	check_stock = 1
# 	# 	check_review = 1

# 	# 	for baris in doc.ste_items:
# 	# 		if not baris.check_qty_stock:
# 	# 			check_pending = 0
# 	# 		if not baris.check_review:
# 	# 			check_stock = 0
# 	# 		if not baris.check_konfirmasi:
# 	# 			check_review = 0

# 	# 	if check_pending == 0:
# 	# 		doc.workflow_state = "Pending"
# 	# 	elif check_stock == 0:
# 	# 		for baris in doc.ste_items:
# 	# 			doctype = doc.chosen_type
# 	# 			if doc.chosen_type == "Stock Entry":
# 	# 				doctype = "Stock Entry Detail"

# 	# 			frappe.db.sql("""
# 	# 				UPDATE `tab{}` 
# 	# 				SET qty = {}
# 	# 				WHERE name = "{}" 
# 	# 			""".format(doctype,baris.qty_stock,baris.qty_stock,baris.sumber_document))

# 	# 		doc.workflow_state = "Persiapan Stock"
# 	# 		frappe.msgprint("State menjadi Persiapan Stock. Stock Entry qty terupdate.")

# 	# 	elif check_review == 0:
# 	# 		doc.workflow_state = "Waiting Review"

# 	# 	elif check_review == 1:
# 	# 		document_asli = frappe.get_doc("Stock Entry", doc.document_number)
# 	# 		document_asli.submit()

# 	# 		doc.workflow_state = "Confirmation"
# 	# 		frappe.msgprint("State menjadi Confirmation. Stock Entry selesai tersubmit.")


# @frappe.whitelist()
# def get_previous_role(workflow_state):
	
# 	confirm1 = ""
# 	confirm2 = ""
# 	get_prev_role = frappe.db.sql(""" SELECT 
# 			wt.allowed FROM `tabWorkflow Transition` wt
# 			JOIN `tabWorkflow` tw ON tw.name = wt.parent
# 			WHERE tw.document_type = "Confirmation Document"
# 			AND tw.is_active = 1
# 			AND wt.next_state = "{}"
# 			AND wt.`action` = "Approve" """.format(workflow_state))
# 	get_current_role = frappe.db.sql(""" SELECT 
# 			wt.allowed FROM `tabWorkflow Transition` wt
# 			JOIN `tabWorkflow` tw ON tw.name = wt.parent
# 			WHERE tw.document_type = "Confirmation Document"
# 			AND tw.is_active = 1
# 			AND wt.state = "{}"
# 			AND wt.`action` = "Approve" """.format(workflow_state))
	
# 	if len(get_prev_role) > 0:
# 		confirm1 = get_prev_role[0][0]

# 	if len(get_current_role) > 0:
# 		confirm2 = get_current_role[0][0]

# 	return [confirm1,confirm2]

# @frappe.whitelist()
# def get_stock_entry_for_confirmation_document(doctype, txt, searchfield, start, page_len, filters):
# 	result = frappe.db.sql("""
# 		SELECT ste.name, ste.purpose
# 		FROM `tabStock Entry` ste 
# 		WHERE ste.name LIKE '%{0}%'
# 		AND ste.docstatus = 0
# 		AND (ste.purpose = "Material Issue" OR ste.purpose = "Material Receipt")
# 		limit {1}, {2}""".format(txt, start, page_len))

# 	return result
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html

@frappe.whitelist()
def update_dn_qty_muat(doc,doctype,qty):
	frappe.db.sql("""
		UPDATE `tab{}` 
		SET qty = {} 
		WHERE name = "{}" 
	""".format(doctype,qty,doc))

@frappe.whitelist()
def on_trash(doc,method):
	frappe.db.sql(""" UPDATE `tab{}` SET confirmation_document = "" WHERE confirmation_document = "{}" and name = "{}" """.format(doc.document_type,doc.name,doc.document_number))

@frappe.whitelist()
def on_cancel(doc, method):
	# if doc.chosen_type != "Delivery Note":
	# 	document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
	# 	# # document_asli.workflow_state = "Cancelled"
	# 	document_asli.cancel()
	pass
	
@frappe.whitelist()
def onload(doc, method):
	if doc.tipe_stock == "Out":
		check_pending = 1
		check_rencana_kirim = 1
		check_stock = 1
		check_muat = 1
		check_validation = 1
		
		for baris in doc.items:
			if not baris.check_rencana_kirim:
				check_pending = 0
			if not baris.checking_stock:
				check_rencana_kirim = 0
			if not baris.check_qty_muat:
				check_stock = 0
			if not baris.check_validasi:
				check_muat = 0
			if not baris.check_konfirmasi:
				check_validation = 0

		if check_pending == 0:
			doc.workflow_state = "Pending"
		elif check_rencana_kirim == 0:
			doc.workflow_state = "Persiapan Rencana Kirim"
		elif check_stock == 0:
			doc.workflow_state = "Checker Stock"
		elif check_muat == 0:
			doc.workflow_state = "Checker Muat"
		elif check_validation == 0:
			doc.workflow_state = "Validation"
		elif check_validation == 1:
			doc.workflow_state = "Confirmation"

	elif doc.tipe_stock == "In":
		check_pending = 1
		check_bongkar = 1
		checking_stock = 1
		check_terima = 1
		check_review = 1
		for baris in doc.pr_items:
			if not baris.check_rencana_bongkar:
				check_pending = 0
			if not baris.checking_stock:
				check_bongkar = 0
			if not baris.check_qty_terima:
				checking_stock = 0
			if not baris.check_review:
				check_terima = 0
			if not baris.check_konfirmasi:
				check_review = 0

		if check_pending == 0:
			doc.workflow_state = "Pending"
		elif check_bongkar == 0:
			doc.workflow_state = "Persiapan Bongkar"
		elif checking_stock == 0:
			doc.workflow_state = "Checker Stock Terima"
		elif check_terima == 0:
			doc.workflow_state = "Persiapan Terima"
		elif check_review == 0:
			doc.workflow_state = "Waiting Review"
		elif check_review == 1:
			doc.workflow_state = "Confirmation"
	
	doc.db_update()


@frappe.whitelist()
def before_submit(doc, method):
	if doc.tipe_stock == "Out":
		check_pending = 1
		check_rencana_kirim = 1
		check_stock = 1
		check_muat = 1
		check_validation = 1
		for baris in doc.items:
			if not baris.check_rencana_kirim:
				check_pending = 0
			if not baris.checking_stock:
				check_rencana_kirim = 0
			if not baris.check_qty_muat:
				check_stock = 0
			if not baris.check_validasi:
				check_muat = 0
			if not baris.check_konfirmasi:
				check_validation = 0

		if check_pending == 0 or check_rencana_kirim == 0 or check_stock == 0 or check_muat == 0 or check_validation == 0:
			frappe.throw("Document tidak bisa tersubmit jika ada centangan yang belum selesai.")
	
	elif doc.tipe_stock == "In":
		check_pending = 1
		check_bongkar = 1
		check_checking_stock = 1
		check_terima = 1
		check_review = 1
		for baris in doc.pr_items:
			if not baris.check_rencana_bongkar:
				check_pending = 0
			if not baris.checking_stock:
				check_bongkar = 0
			if not baris.check_qty_terima:
				check_checking_stock = 0
			if not baris.check_review:
				check_terima = 0
			if not baris.check_konfirmasi:
				check_review = 0

		if check_pending == 0 or check_bongkar == 0 or check_checking_stock == 0 or check_terima == 0 or check_review == 0:
			frappe.throw("Document tidak bisa tersubmit jika ada centangan yang belum selesai.")
		

@frappe.whitelist()
def validate(doc, method):
	document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
	document_asli.confirmation_document = doc.name
	document_asli.db_update()

	if doc.tipe_stock == "Out":
		check_pending = 1
		check_rencana_kirim = 1
		check_stock = 1
		check_muat = 1
		check_validation = 1
		
		for baris in doc.items:
			if not baris.check_rencana_kirim:
				check_pending = 0
			if not baris.checking_stock:
				check_rencana_kirim = 0
			if not baris.check_qty_muat:
				check_stock = 0
			if not baris.check_validasi:
				check_muat = 0
			if not baris.check_konfirmasi:
				check_validation = 0

		if check_pending == 0:
			doc.workflow_state = "Pending"
		elif check_rencana_kirim == 0:
			doc.workflow_state = "Persiapan Rencana Kirim"
			if doc.chosen_type == "Delivery Note":
				frappe.db.sql("""
					UPDATE `tabDelivery Note` 
					SET workflow_state = "Pending"
					WHERE name = "{}" 
				""".format(doc.document_number))
		elif check_stock == 0:
			doc.workflow_state = "Checker Stock"
			if doc.chosen_type == "Delivery Note":
				frappe.db.sql("""
					UPDATE `tabDelivery Note` 
					SET workflow_state = "In Confirmation Doc"
					WHERE name = "{}" 
				""".format(doc.document_number))

				for baris in doc.items:
					doctype = "Delivery Note Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}, keterangan_check = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_rencana_kirim,baris.keterangan_checking_stock,baris.sumber_document))

				dn = frappe.get_doc("Delivery Note",doc.document_number)
				for i in dn.items:
					i.amount = i.qty * i.rate

				dn.flags.ignore_permission = True
				dn.save()

				frappe.msgprint("State menjadi Checker Stock. Delivery Note qty terupdate.")

			elif doc.chosen_type == "Purchase Receipt":
				for baris in doc.items:
					doctype = "Purchase Receipt Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {} * -1, received_qty = {} * -1, keterangan_check = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_rencana_kirim,baris.qty_rencana_kirim,baris.keterangan_checking_stock,baris.sumber_document))
				frappe.msgprint("State menjadi Checker Stock. Purchase Receipt qty terupdate.")

			elif doc.chosen_type == "Stock Entry":
				for baris in doc.items:
					doctype = "Stock Entry Detail"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}
						WHERE name = "{}" 
					""".format(doctype,baris.qty_rencana_kirim,baris.sumber_document))
				frappe.msgprint("State menjadi Checker Stock. Stock Entry qty terupdate.")
		elif check_muat == 0:
			if doc.chosen_type == "Delivery Note":
				frappe.db.sql("""
					UPDATE `tabDelivery Note` 
					SET workflow_state = "In Confirmation Doc"
					WHERE name = "{}" 
				""".format(doc.document_number))

				for baris in doc.items:
					doctype = "Delivery Note Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}, keterangan_muat = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_muat,baris.keterangan_muat,baris.sumber_document))

				dn = frappe.get_doc("Delivery Note",doc.document_number)
				for i in dn.items:
					i.amount = i.qty * i.rate

				dn.flags.ignore_permission = True
				dn.save()

				frappe.msgprint("State menjadi Checker Muat. Delivery Note qty terupdate.")

			elif doc.chosen_type == "Purchase Receipt":
				for baris in doc.items:
					doctype = "Purchase Receipt Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {} * -1, received_qty = {} * -1, keterangan_muat = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_muat,baris.qty_muat,baris.keterangan_muat,baris.sumber_document))
				frappe.msgprint("State menjadi Checker Muat. Purchase Receipt qty terupdate.")

			elif doc.chosen_type == "Stock Entry":
				for baris in doc.items:
					doctype = "Stock Entry Detail"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}
						WHERE name = "{}" 
					""".format(doctype,baris.qty_muat,baris.sumber_document))
				frappe.msgprint("State menjadi Checker Muat. Stock Entry qty terupdate.")
			doc.workflow_state = "Checker Muat"
			
		elif check_validation == 0:
			if doc.chosen_type == "Delivery Note":
				frappe.db.sql("""
					UPDATE `tabDelivery Note` 
					SET workflow_state = "In Confirmation Doc"
					WHERE name = "{}" 
				""".format(doc.document_number))
			# frappe.db.sql(""" UPDATE `tab{}` SET workflow_state = "{}" WHERE name = "{}" """.format(doc.chosen_type,"Print DN",doc.document_number))
			doc.workflow_state = "Validation"

		elif check_validation == 1:
			document_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
			if doc.chosen_type == "Delivery Note":
				document_asli.workflow_state = "Print DN"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi Print DN.".format(doc.chosen_type))
			elif doc.chosen_type == "Purchase Receipt":
				document_asli.workflow_state = "In Purchasing"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi In Purchasing.".format(doc.chosen_type))
			else:
				# document_asli.workflow_state = "Pending"
				# document_asli.db_update()
				# document_asli.submit()
				# document_asli.workflow_state = "Submitted"
				# doc.submit()
				# frappe.msgprint("State menjadi Confirmation. {} selesai tersubmit.".format(doc.chosen_type))
				document_asli.workflow_state = "In DIC"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi In DIC.".format(doc.chosen_type))


	elif doc.tipe_stock == "In":
		check_pending = 1
		check_bongkar = 1
		check_checking_stock = 1
		check_terima = 1
		check_review = 1
		for baris in doc.pr_items:
			if not baris.check_rencana_bongkar:
				check_pending = 0
			if not baris.checking_stock:
				check_bongkar = 0
			if not baris.check_qty_terima:
				check_checking_stock = 0
			if not baris.check_review:
				check_terima = 0
			if not baris.check_konfirmasi:
				check_review = 0

		if check_pending == 0:
			doc.workflow_state = "Pending"
		elif check_bongkar == 0:
			doc.workflow_state = "Persiapan Bongkar"
		elif check_checking_stock == 0:
			doc.workflow_state = "Checker Stock Terima"

			if doc.chosen_type == "Delivery Note":
				for baris in doc.items:
					doctype = "Delivery Note Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {} * -1, keterangan_check = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_rencana_terima,baris.keterangan_checking_stock,baris.sumber_document))
				
				dn = frappe.get_doc("Delivery Note",doc.document_number)
				for i in dn.items:
					i.amount = i.qty * i.rate

				dn.flags.ignore_permission = True
				dn.save()
				frappe.msgprint("State menjadi Checker Stock Terima. Delivery Note qty terupdate.")

			elif doc.chosen_type == "Purchase Receipt":
				for baris in doc.items:
					doctype = "Purchase Receipt Item"
					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}, received_qty = {}, keterangan_check = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_rencana_terima,baris.qty_rencana_terima,baris.keterangan_checking_stock,baris.sumber_document))
				frappe.msgprint("State menjadi Checker Stock Terima. Purchase Receipt qty terupdate.")

		elif check_terima == 0:
			doc.workflow_state = "Persiapan Terima"

			if doc.chosen_type == "Delivery Note":
				for baris in doc.pr_items:
					doctype = doc.chosen_type
					if doc.chosen_type == "Delivery Note":
						doctype = "Delivery Note Item"

					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {} * -1, keterangan_muat = "{}" 
						WHERE name = "{}" 
					""".format(doctype,baris.qty_terima,baris.keterangan_terima,baris.sumber_document))
				dn = frappe.get_doc("Delivery Note",doc.document_number)
				for i in dn.items:
					i.amount = i.qty * i.rate

				dn.flags.ignore_permission = True
				dn.save()
				frappe.msgprint("State menjadi Persiapan Terima. Delivery Note qty terupdate.")

			elif doc.chosen_type == "Purchase Receipt":
				for baris in doc.pr_items:
					doctype = doc.chosen_type
					if doc.chosen_type == "Purchase Receipt":
						doctype = "Purchase Receipt Item"

					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}, received_qty = {}, keterangan_muat = "{}"
						WHERE name = "{}" 
					""".format(doctype,baris.qty_terima,baris.qty_terima,baris.keterangan_terima,baris.sumber_document))
				frappe.msgprint("State menjadi Persiapan Terima. Purchase Receipt qty terupdate.")

			elif doc.chosen_type == "Stock Entry":
				for baris in doc.pr_items:
					doctype = doc.chosen_type
					if doc.chosen_type == "Stock Entry":
						doctype = "Stock Entry Detail"

					frappe.db.sql("""
						UPDATE `tab{}` 
						SET qty = {}
						WHERE name = "{}" 
					""".format(doctype,baris.qty_terima,baris.sumber_document))
				frappe.msgprint("State menjadi Persiapan Terima. Stock Entry qty terupdate.")

		elif check_review == 0:
			doc.workflow_state = "Waiting Review"
			
		elif check_review == 1:
			ddocument_asli = frappe.get_doc(doc.chosen_type, doc.document_number)
			if doc.chosen_type == "Delivery Note":
				document_asli.workflow_state = "Print DN"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi Print DN.".format(doc.chosen_type))
			elif doc.chosen_type == "Purchase Receipt":
				document_asli.workflow_state = "In Purchasing"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi In Purchasing.".format(doc.chosen_type))
			else:
				# document_asli.workflow_state = "Pending"
				# document_asli.db_update()
				# document_asli.submit()
				# document_asli.workflow_state = "Submitted"
				# doc.submit()
				# frappe.msgprint("State menjadi Confirmation. {} selesai tersubmit.".format(doc.chosen_type))
				document_asli.workflow_state = "In DIC"
				document_asli.db_update()
				doc.submit()
				frappe.msgprint("State menjadi Confirmation. {} menjadi In DIC.".format(doc.chosen_type))

	doc.db_update()
	# elif doc.chosen_type == "Stock Entry":
	# 	check_pending = 1
	# 	check_stock = 1
	# 	check_review = 1

	# 	for baris in doc.ste_items:
	# 		if not baris.check_qty_stock:
	# 			check_pending = 0
	# 		if not baris.check_review:
	# 			check_stock = 0
	# 		if not baris.check_konfirmasi:
	# 			check_review = 0

	# 	if check_pending == 0:
	# 		doc.workflow_state = "Pending"
	# 	elif check_stock == 0:
	# 		for baris in doc.ste_items:
	# 			doctype = doc.chosen_type
	# 			if doc.chosen_type == "Stock Entry":
	# 				doctype = "Stock Entry Detail"

	# 			frappe.db.sql("""
	# 				UPDATE `tab{}` 
	# 				SET qty = {}
	# 				WHERE name = "{}" 
	# 			""".format(doctype,baris.qty_stock,baris.qty_stock,baris.sumber_document))

	# 		doc.workflow_state = "Persiapan Stock"
	# 		frappe.msgprint("State menjadi Persiapan Stock. Stock Entry qty terupdate.")

	# 	elif check_review == 0:
	# 		doc.workflow_state = "Waiting Review"

	# 	elif check_review == 1:
	# 		document_asli = frappe.get_doc("Stock Entry", doc.document_number)
	# 		document_asli.submit()

	# 		doc.workflow_state = "Confirmation"
	# 		frappe.msgprint("State menjadi Confirmation. Stock Entry selesai tersubmit.")


@frappe.whitelist()
def get_previous_role(workflow_state):
	
	confirm1 = ""
	confirm2 = ""
	get_prev_role = frappe.db.sql(""" SELECT 
			wt.allowed FROM `tabWorkflow Transition` wt
			JOIN `tabWorkflow` tw ON tw.name = wt.parent
			WHERE tw.document_type = "Confirmation Document"
			AND tw.is_active = 1
			AND wt.next_state = "{}"
			AND wt.`action` = "Approve" """.format(workflow_state))
	get_current_role = frappe.db.sql(""" SELECT 
			wt.allowed FROM `tabWorkflow Transition` wt
			JOIN `tabWorkflow` tw ON tw.name = wt.parent
			WHERE tw.document_type = "Confirmation Document"
			AND tw.is_active = 1
			AND wt.state = "{}"
			AND wt.`action` = "Approve" """.format(workflow_state))
	
	if len(get_prev_role) > 0:
		confirm1 = get_prev_role[0][0]

	if len(get_current_role) > 0:
		confirm2 = get_current_role[0][0]

	return [confirm1,confirm2]

@frappe.whitelist()
def get_stock_entry_for_confirmation_document(doctype, txt, searchfield, start, page_len, filters):
	result = frappe.db.sql("""
		SELECT ste.name, ste.purpose
		FROM `tabStock Entry` ste 
		WHERE ste.name LIKE '%{0}%'
		AND ste.docstatus = 0
		AND (ste.purpose = "Material Issue" OR ste.purpose = "Material Receipt")
		limit {1}, {2}""".format(txt, start, page_len))

	return result
