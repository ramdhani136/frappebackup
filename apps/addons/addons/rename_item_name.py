from __future__ import unicode_literals
import frappe
import pandas as pd
# from frappe.model.document import Document
# from datetime import date
# import datetime
# from erpnext.accounts.utils import get_fiscal_years, validate_fiscal_year, get_account_currency
# from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
# from frappe.utils import cint, flt, getdate, add_days, cstr, nowdate, get_link_to_form, formatdate
# from erpnext.accounts.general_ledger import make_gl_entries

# etm
@frappe.whitelist()
def rename():
	#isi
	item_code = ["019075010000-410093T-S32"]
	name_baru = "KP KNT ALEA TABENG HITAM 410093T-S32"
	
	col = ["Name","Item_Name","Item_Group"]
	data = pd.read_excel (r'/home/frappe/frappe-bench/apps/addons/addons/patch_itemname_etm.xls') 
	df = pd.DataFrame(data, columns= col)
	
	
	for idx in range(len(df)):
		#Item 
		# doc_item = frappe.get_doc('Item',{'item_code': d})
		# if doc_item:
		# 	print("masuk item")
		# 	doc_item.stock_uom = uom_baru
		# 	doc_item.db_update()
		# 	print(d+ " berhasil di rubah")

		#purchase invoice
		data_pi = frappe.db.sql(""" SELECT * from `tabPurchase Invoice Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_pi:
			print("masuk pinv")
			for i in data_pi:
				doc_pi = frappe.get_doc('Purchase Invoice Item',i['name'])
				doc_pi.item_name = df[col[1]][idx]
				doc_pi.item_group = df[col[2]][idx]
				doc_pi.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")
				
		#purchase recipt
		data_pr = frappe.db.sql(""" SELECT * from `tabPurchase Receipt Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_pr:
			print("masuk pr")
			for i in data_pr:
				doc_pr = frappe.get_doc('Purchase Receipt Item',i['name'])
				doc_pr.item_name = df[col[1]][idx]
				doc_pr.item_group = df[col[2]][idx]
				doc_pr.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		# purchase order
		data_po = frappe.db.sql(""" SELECT * from `tabPurchase Order Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_po:
			print("masuk po")
			for i in data_po:
				doc_po = frappe.get_doc('Purchase Order Item',i['name'])
				doc_po.item_name = df[col[1]][idx]
				doc_po.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")
		
		#Sales Invoice
		data_si = frappe.db.sql(""" SELECT * from `tabSales Invoice Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_si:
			print("masuk sinv")
			for i in data_si:
				doc_si = frappe.get_doc('Sales Invoice Item',i['name'])
				doc_si.item_name = df[col[1]][idx]
				# doc_si.item_group = df[col[2]][idx]
				doc_si.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#Sales Order Item
		data_so = frappe.db.sql(""" SELECT * from `tabSales Order Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_so:
			print("masuk so")
			for i in data_so:
				doc_so = frappe.get_doc('Sales Order Item',i['name'])
				doc_so.item_name = df[col[1]][idx]
				doc_so.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#Delivery Note Item
		data_dn = frappe.db.sql(""" SELECT * from `tabDelivery Note Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_dn:
			print("masuk dn")
			for i in data_dn:
				doc_dn = frappe.get_doc('Delivery Note Item',i['name'])
				doc_dn.item_name = df[col[1]][idx]
				doc_dn.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#Packed Item
		data_pac = frappe.db.sql(""" SELECT * from `tabPacked Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_pac:
			print("masuk package")
			for i in data_pac:
				doc_pac = frappe.get_doc('Packed Item',i['name'])
				doc_pac.item_name = df[col[1]][idx]
				doc_pac.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#Stock Entry Detail
		data_se = frappe.db.sql(""" SELECT * from `tabStock Entry Detail` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_se:
			print('masuk sed')
			for i in data_se:
				doc_se = frappe.get_doc('Stock Entry Detail',i['name'])
				doc_se.item_name = df[col[1]][idx]
				doc_se.item_group = df[col[2]][idx]
				doc_se.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#Stock Ledger Entry
		# data_sle = frappe.db.sql(""" SELECT name,item_code from `tabStock Ledger Entry` where item_code='{0}' """.format(d),as_dict=1)
		# if data_sle:
		# 	print("masuk sle")
		# 	for i in data_sle:
		# 		doc_sle = frappe.get_doc('Stock Ledger Entry',i['name'])
		# 		doc_sle.item_name = name_baru
		# 		doc_sle.db_update()
		# 		print(d+ " berhasil di rubah")

		#Bin
		# data_b = frappe.db.sql(""" SELECT name,item_code from `tabBin` where item_code='{0}' """.format(d),as_dict=1)
		# if data_b:
		# 	print("masuk bin")
		# 	for i in data_b:
		# 		doc_b = frappe.get_doc('Bin',i['name'])
		# 		doc_b.stock_uom = uom_baru
		# 		# doc_b.uom = uom_baru
		# 		doc_b.db_update()
		# 		print(d+ " berhasil di rubah")

		#Product Bundle Item
		# data_pb = frappe.db.sql(""" SELECT name,item_code from `tabProduct Bundle Item` where item_code='{0}' """.format(d),as_dict=1)
		# if data_pb:
		# 	print("masuk bundle")
		# 	for i in data_pb:
		# 		doc_pb = frappe.get_doc('Product Bundle Item',i['name'])
		# 		# doc_pb.stock_uom = uom_baru
		# 		doc_pb.uom = uom_baru
		# 		doc_pb.db_update()
		# 		print(d+ " berhasil di rubah")

		#BOM Item
		data_bi = frappe.db.sql(""" SELECT * from `tabBOM Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_bi:
			print("masuk bom")
			for i in data_bi:
				doc_bi = frappe.get_doc('BOM Item',i['name'])
				doc_bi.item_name = df[col[1]][idx]
				doc_bi.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")

		#UOM Conversion Detail
		# data_ucd = frappe.db.sql(""" SELECT * from `tabUOM Conversion Detail` where parent='{0}' """.format(d),as_dict=1)
		# if data_ucd:
		# 	for i in data_ucd:
		# 		if i['conversion_factor'] == 1:
		# 			print('masuk ucd')
		# 			doc_ucd = frappe.get_doc('UOM Conversion Detail',i['name'])
		# 			# doc_ucd.stock_uom = uom_baru
		# 			doc_ucd.uom = uom_baru
		# 			doc_ucd.db_update()
		# 			print(d+ " berhasil di rubah")

		#Material Request Item
		data_mri = frappe.db.sql(""" SELECT * from `tabMaterial Request Item` where item_code='{0}' """.format(df[col[0]][idx]),as_dict=1)
		if data_mri:
			print("masuk mri")
			for i in data_mri:
				doc_mri = frappe.get_doc('Material Request Item',i['name'])
				doc_mri.item_name = df[col[1]][idx]
				doc_mri.item_group = df[col[2]][idx]
				doc_mri.db_update()
				print(df[col[0]][idx]+ " berhasil di rubah")
		

@frappe.whitelist()
def rename_kode():
	col = ["Name", "New_Name", "Item_Name", "UOM", "Stocker", "Item_Group"]
	data = pd.read_excel (r'/home/frappe/frappe-bench/apps/addons/addons/patch_item_etm.xls', dtype={'Name': str, "New_Name": str}) 
	df = pd.DataFrame(data, columns=col)

	for index, row in df.iterrows():
		name = row['Name']
		if not pd.isna(row['New_Name']):
			frappe.rename_doc("Item", row['Name'], row['New_Name'])
			name = row['New_Name']

		doc_item = frappe.get_doc('Item', { 'item_code': name  })
		if doc_item:
			print("masuk item")
			if not pd.isna(row['Item_Name']):
				doc_item.item_name = row['Item_Name']
			if not pd.isna(row['UOM']):
				doc_item.stock_uom = row['UOM']
			if not pd.isna(row['Stocker']):
				doc_item.stocker = row['Stocker']
			doc_item.db_update()
			print(row['Name']+ " berhasil di rubah")

		#item price
		data_ip = frappe.db.sql(""" SELECT * from `tabItem Price` where item_code='{0}' """.format(name),as_dict=1)
		if data_ip:
			print("masuk item price")
			for i in data_ip:
				doc_ip = frappe.get_doc('Item Price',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_ip.item_name = row['Item_Name']
				doc_ip.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		#puchase invoice
		data_pi = frappe.db.sql(""" SELECT * from `tabPurchase Invoice Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_pi:
			print("masuk pinv")
			for i in data_pi:
				doc_pi = frappe.get_doc('Purchase Invoice Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_pi.item_name = row['Item_Name']
				if not pd.isna(row['Item_Group']):
					doc_pi.item_group = row['Item_Group']
				if not pd.isna(row['UOM']):
					doc_pi.stock_uom = row['UOM']
				doc_pi.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

				
		#purchase recipt
		data_pr = frappe.db.sql(""" SELECT * from `tabPurchase Receipt Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_pr:
			print("masuk pr")
			for i in data_pr:
				doc_pr = frappe.get_doc('Purchase Receipt Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_pr.item_name = row['Item_Name']
				if not pd.isna(row['Item_Group']):
					doc_pr.item_group = row['Item_Group']
				if not pd.isna(row['UOM']):
					data_pr.stock_uom = row['UOM']
				doc_pr.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		# purchase order
		data_po = frappe.db.sql(""" SELECT * from `tabPurchase Order Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_po:
			print("masuk po")
			for i in data_po:
				doc_po = frappe.get_doc('Purchase Order Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_po.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_po.stock_uom = row['UOM']
				doc_po.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		
		#Sales Invoice
		data_si = frappe.db.sql(""" SELECT * from `tabSales Invoice Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_si:
			print("masuk sinv")
			for i in data_si:
				doc_si = frappe.get_doc('Sales Invoice Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_si.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_si.stock_uom = row['UOM']
				# doc_si.item_group = df[col[2]][idx]
				doc_si.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		#Sales Order Item
		data_so = frappe.db.sql(""" SELECT * from `tabSales Order Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_so:
			print("masuk so")
			for i in data_so:
				doc_so = frappe.get_doc('Sales Order Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_so.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_so.stock_uom = row['UOM']
				doc_so.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		#Delivery Note Item
		data_dn = frappe.db.sql(""" SELECT * from `tabDelivery Note Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_dn:
			print("masuk dn")
			for i in data_dn:
				doc_dn = frappe.get_doc('Delivery Note Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_dn.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_dn.stock_uom = row['UOM']
				doc_dn.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		#Packed Item
		data_pac = frappe.db.sql(""" SELECT * from `tabPacked Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_pac:
			print("masuk package")
			for i in data_pac:
				doc_pac = frappe.get_doc('Packed Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_pac.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_pac.stock_uom = row['UOM']
					if not (i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1):
						doc_pac.uom = row['UOM']
				doc_pac.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))


		#Stock Entry Detail
		data_se = frappe.db.sql(""" SELECT * from `tabStock Entry Detail` where item_code='{0}' """.format(name),as_dict=1)
		if data_se:
			print('masuk sed')
			for i in data_se:
				doc_se = frappe.get_doc('Stock Entry Detail',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_se.item_name = row['Item_Name']
				if not pd.isna(row['Item_Group']):
					doc_se.item_group = row['Item_Group']
				if not pd.isna(row['UOM']):
					doc_se.stock_uom = row['UOM']
					if not (i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1):
						doc_se.uom = row['UOM']
				doc_se.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#Stock Ledger Entry
		if not pd.isna(row['UOM']):
			data_sle = frappe.db.sql(""" SELECT name,item_code from `tabStock Ledger Entry` where item_code='{0}' """.format(name),as_dict=1)
			if data_sle:
				print("masuk sle")
				for i in data_sle:
					doc_sle = frappe.get_doc('Stock Ledger Entry',i['name'])
					if not pd.isna(row['UOM']):
						doc_sle.stock_uom = row['UOM']
					doc_sle.db_update()
					print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#Bin
		if not pd.isna(row['UOM']):
			data_b = frappe.db.sql(""" SELECT name,item_code from `tabBin` where item_code='{0}' """.format(name),as_dict=1)
			if data_b:
				print("masuk bin")
				for i in data_b:
					doc_b = frappe.get_doc('Bin',i['name'])
					doc_b.stock_uom = row['UOM']
					# doc_b.uom = uom_baru
					doc_b.db_update()
					print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#Product Bundle Item
		if not pd.isna(row['UOM']):
			data_pb = frappe.db.sql(""" SELECT name,item_code from `tabProduct Bundle Item` where item_code='{0}' """.format(name),as_dict=1)
			if data_pb:
				print("masuk bundle")
				for i in data_pb:
					doc_pb = frappe.get_doc('Product Bundle Item',i['name'])
					# doc_pb.stock_uom = uom_baru
					doc_pb.uom = row['UOM']
					doc_pb.db_update()
					print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#BOM Item
		data_bom = frappe.db.sql(""" SELECT * from `tabBOM` where item='{0}' """.format(name),as_dict=1)
		if data_bom:
			print("masuk bom")
			for i in data_bom:
				doc_bom = frappe.get_doc('BOM',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_bom.item_name = row['Item_Name']
				doc_bom.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#BOM Item
		data_bi = frappe.db.sql(""" SELECT * from `tabBOM Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_bi:
			print("masuk bom")
			for i in data_bi:
				doc_bi = frappe.get_doc('BOM Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_bi.item_name = row['Item_Name']
				if not pd.isna(row['UOM']):
					doc_se.stock_uom = row['UOM']
					if not (i['stock_uom'] != i['uom'] and i['conversion_factor'] != 1):
						doc_se.uom = row['UOM']
				doc_bi.db_update()
				print("Item {} pada doc {} berhasil di rubah".format(name, i['name']))

		#UOM Conversion Detail
		if not pd.isna(row['UOM']):
			data_ucd = frappe.db.sql(""" SELECT * from `tabUOM Conversion Detail` where parent='{0}' """.format(name),as_dict=1)
			if data_ucd:
				for i in data_ucd:
					if i['conversion_factor'] == 1:
						print('masuk ucd')
						doc_ucd = frappe.get_doc('UOM Conversion Detail',i['name'])
						# doc_ucd.stock_uom = uom_baru
						doc_ucd.uom = row['UOM']
						doc_ucd.db_update()
						print(d+ " berhasil di rubah")

		#Material Request Item
		data_mri = frappe.db.sql(""" SELECT * from `tabMaterial Request Item` where item_code='{0}' """.format(name),as_dict=1)
		if data_mri:
			print("masuk mri")
			for i in data_mri:
				doc_mri = frappe.get_doc('Material Request Item',i['name'])
				if not pd.isna(row['Item_Name']):
					doc_mri.item_name = row['Item_Name']
				if not pd.isna(row['Item_Group']):
					doc_mri.item_group = row['Item_Group']
				doc_mri.db_update()
				print(name+ " berhasil di rubah")


