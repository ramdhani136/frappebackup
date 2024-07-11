from __future__ import unicode_literals
import frappe
# from frappe.model.document import Document
# from datetime import date
# import datetime
# from erpnext.accounts.utils import get_fiscal_years, validate_fiscal_year, get_account_currency
# from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
# from frappe.utils import cint, flt, getdate, add_days, cstr, nowdate, get_link_to_form, formatdate
# from erpnext.accounts.general_ledger import make_gl_entries

# gracia
@frappe.whitelist()
def rename():
	#isi
	item_code = ["022148006000"]
	uom_baru = "MTR"
	
	for d in item_code:
		#Item 
		doc_item = frappe.get_doc('Item',{'item_code': d})
		if doc_item:
			frappe.msgprint("masuk item")
			doc_item.stock_uom = uom_baru
			doc_item.db_update()
			frappe.msgprint(d+ "berhasil di rubah")

		#purchase invoice
		data_pi = frappe.db.sql(""" SELECT * from `tabPurchase Invoice Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_pi:
			frappe.msgprint("masuk pinv")
			for i in data_pi:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_pi = frappe.get_doc('Purchase Invoice Item',i['name'])
					doc_pi.stock_uom = uom_baru
					# doc_pi.uom = uom_baru
					doc_pi.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_pi = frappe.get_doc('Purchase Invoice Item',i['name'])
					doc_pi.stock_uom = uom_baru
					doc_pi.uom = uom_baru
					doc_pi.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#purchase recipt
		data_pr = frappe.db.sql(""" SELECT * from `tabPurchase Receipt Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_pr:
			frappe.msgprint("masuk pr")
			for i in data_pr:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_pr = frappe.get_doc('Purchase Receipt Item',i['name'])
					doc_pr.stock_uom = uom_baru
					# doc_pr.uom = uom_baru
					doc_pr.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_pr = frappe.get_doc('Purchase Receipt Item',i['name'])
					doc_pr.stock_uom = uom_baru
					doc_pr.uom = uom_baru
					doc_pr.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		# purchase order
		data_po = frappe.db.sql(""" SELECT * from `tabPurchase Order Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_po:
			frappe.msgprint("masuk po")
			for i in data_po:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_po = frappe.get_doc('Purchase Order Item',i['name'])
					doc_po.stock_uom = uom_baru
					# doc_po.uom = uom_baru
					doc_po.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_po = frappe.get_doc('Purchase Order Item',i['name'])
					doc_po.stock_uom = uom_baru
					doc_po.uom = uom_baru
					doc_po.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
		
		#Sales Invoice
		data_si = frappe.db.sql(""" SELECT * from `tabSales Invoice Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_si:
			frappe.msgprint("masuk sinv")
			for i in data_si:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_si = frappe.get_doc('Sales Invoice Item',i['name'])
					doc_si.stock_uom = uom_baru
					# doc_si.uom = uom_baru
					doc_si.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_si = frappe.get_doc('Sales Invoice Item',i['name'])
					doc_si.stock_uom = uom_baru
					doc_si.uom = uom_baru
					doc_si.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#Sales Order Item
		data_so = frappe.db.sql(""" SELECT * from `tabSales Order Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_so:
			frappe.msgprint("masuk so")
			for i in data_so:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_so = frappe.get_doc('Sales Order Item',i['name'])
					doc_so.stock_uom = uom_baru
					# doc_so.uom = uom_baru
					doc_so.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_so = frappe.get_doc('Sales Order Item',i['name'])
					doc_so.stock_uom = uom_baru
					doc_so.uom = uom_baru
					doc_so.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#Delivery Note Item
		data_dn = frappe.db.sql(""" SELECT * from `tabDelivery Note Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_dn:
			frappe.msgprint("masuk dn")
			for i in data_dn:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_dn = frappe.get_doc('Delivery Note Item',i['name'])
					doc_dn.stock_uom = uom_baru
					# doc_dn.uom = uom_baru
					doc_dn.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_dn = frappe.get_doc('Delivery Note Item',i['name'])
					doc_dn.stock_uom = uom_baru
					doc_dn.uom = uom_baru
					doc_dn.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#Packed Item
		data_pac = frappe.db.sql(""" SELECT * from `tabPacked Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_pac:
			frappe.msgprint("masuk package")
			for i in data_pac:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_pac = frappe.get_doc('Packed Item',i['name'])
					doc_pac.stock_uom = uom_baru
					# doc_pac.uom = uom_baru
					doc_pac.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_pac = frappe.get_doc('Packed Item',i['name'])
					doc_pac.stock_uom = uom_baru
					doc_pac.uom = uom_baru
					doc_pac.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#Stock Entry Detail
		data_se = frappe.db.sql(""" SELECT * from `tabStock Entry Detail` where item_code='{0}' """.format(d),as_dict=1)
		if data_se:
			frappe.msgprint('masuk sed')
			for i in data_se:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_se = frappe.get_doc('Stock Entry Detail',i['name'])
					doc_se.stock_uom = uom_baru
					# doc_se.uom = uom_baru
					doc_se.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_se = frappe.get_doc('Stock Entry Detail',i['name'])
					doc_se.stock_uom = uom_baru
					doc_se.uom = uom_baru
					doc_se.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#Stock Ledger Entry
		data_sle = frappe.db.sql(""" SELECT name,item_code from `tabStock Ledger Entry` where item_code='{0}' """.format(d),as_dict=1)
		if data_sle:
			frappe.msgprint("masuk sle")
			for i in data_sle:
				doc_sle = frappe.get_doc('Stock Ledger Entry',i['name'])
				doc_sle.stock_uom = uom_baru
				# doc_se.uom = uom_baru
				doc_sle.db_update()
				frappe.msgprint(d+ "berhasil di rubah")

		#Bin
		data_b = frappe.db.sql(""" SELECT name,item_code from `tabBin` where item_code='{0}' """.format(d),as_dict=1)
		if data_b:
			frappe.msgprint("masuk bin")
			for i in data_b:
				doc_b = frappe.get_doc('Bin',i['name'])
				doc_b.stock_uom = uom_baru
				# doc_b.uom = uom_baru
				doc_b.db_update()
				frappe.msgprint(d+ "berhasil di rubah")

		#Product Bundle Item
		data_pb = frappe.db.sql(""" SELECT name,item_code from `tabProduct Bundle Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_pb:
			frappe.msgprint("masuk bundle")
			for i in data_pb:
				doc_pb = frappe.get_doc('Product Bundle Item',i['name'])
				# doc_pb.stock_uom = uom_baru
				doc_pb.uom = uom_baru
				doc_pb.db_update()
				frappe.msgprint(d+ "berhasil di rubah")

		#BOM Item
		data_bi = frappe.db.sql(""" SELECT * from `tabBOM Item` where item_code='{0}' """.format(d),as_dict=1)
		if data_bi:
			frappe.msgprint("masuk bom")
			for i in data_bi:
				if i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1:
					doc_bi = frappe.get_doc('BOM Item',i['name'])
					doc_bi.stock_uom = uom_baru
					# doc_bi.uom = uom_baru
					doc_bi.db_update()
					frappe.msgprint(d+ "berhasil di rubah")
				else:
					doc_bi = frappe.get_doc('BOM Item',i['name'])
					doc_bi.stock_uom = uom_baru
					doc_bi.uom = uom_baru
					doc_bi.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		#UOM Conversion Detail
		data_ucd = frappe.db.sql(""" SELECT * from `tabUOM Conversion Detail` where parent='{0}' """.format(d),as_dict=1)
		if data_ucd:
			for i in data_ucd:
				if i['conversion_factor'] == 1:
					frappe.msgprint('masuk ucd')
					doc_ucd = frappe.get_doc('UOM Conversion Detail',i['name'])
					# doc_ucd.stock_uom = uom_baru
					doc_ucd.uom = uom_baru
					doc_ucd.db_update()
					frappe.msgprint(d+ "berhasil di rubah")

		


