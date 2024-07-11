from __future__ import unicode_literals
import frappe
import math
from frappe import _

def cancel_delete_doc():
	doctype = 'Item'
	list_doc = frappe.db.sql_list(""" SELECT NAME FROM `tab{}` ORDER BY NAME DESC """.format(doctype))
	print (len(list_doc))
	for i in list_doc:
		doc = frappe.get_doc('Item',i)
		doc.delete()
		print (doc.name, " DONE")
		frappe.db.commit()

#def dn_autoname(self, method):
#    frappe.msgprint('Tes')
def patch_account():
	frappe.db.sql("update `tabDelivery Note Item` si inner join tabItem i on si.item_code=i.name set si.item_group =i.item_group where si.item_group!=i.item_group",as_list=1)
	frappe.db.sql("update `tabSales Invoice Item` si inner join tabItem i on si.item_code=i.name set si.item_group =i.item_group where si.item_group!=i.item_group",as_list=1)
	print("set")
	data=frappe.db.sql("""select income_account,parent,expense_account from `tabItem Default` where parenttype="Item Group" """,as_list=1)
	for row in data:
		if row[0]:
			frappe.db.sql("""update `tabSales Invoice Item` set income_account="{}" where item_group="{}" """.format(row[0],row[1]))
		if row[2]:
			frappe.db.sql("""update `tabDelivery Note Item` set expense_account="{}" where item_group="{}" """.format(row[2],row[1]))
		frappe.db.commit()
def patch_data():
	docs=["Stock Entry","Sales Invoice","Delivery Note"]
#	docname="SJ-2022-09-00199"
	#data=frappe.db.sql("select name from `tab{}` where docstatus=1 and purpose ='Manufacture' ".format(doctype),as_list=1)
	#total=len(data)
	for doctype in docs:
		data=[]
		if doctype=="Stock Entry":
			data=frappe.db.sql("select name from `tab{}` where docstatus=1 and purpose ='Manufacture' ".format(doctype),as_list=1)
		else:
			data=frappe.db.sql("select name from `tab{}` where docstatus=1 ".format(doctype),as_list=1)
		total=len(data)
		index=0
		print("Start {}".format(doctype))
		for row in data:
			docname=row[0]
			docu = frappe.get_doc(doctype, docname)
			delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
			docu.make_gl_entries()
			frappe.db.commit()
			index=index+1
			print("{} of {}".format(index,total))

@frappe.whitelist()
def operasi_stock_ledger():
	list_voucher = frappe.db.sql(""" 
		SELECT voucher_type, voucher_no,
		TIMESTAMP(posting_date,posting_time) FROM `tabStock Ledger Entry` WHERE
		docstatus = 2 AND is_cancelled = 0
		GROUP BY voucher_no
		ORDER BY TIMESTAMP(posting_date,posting_time) """)

	for row in list_voucher:
		repair_gl_entry_tanpa_repost(row[0],row[1])
		print("{}={}".format(row[0],row[1]))
		frappe.db.commit()


@frappe.whitelist()
def repair_gl_entry_tanpa_repost(doctype,docname):
	
	docu = frappe.get_doc(doctype, docname)	
	if doctype == "Stock Entry":
		if docu.purpose == "Material Transfer":
			docu.calculate_rate_and_amount()
			for row in docu.items:
				row.db_update()

			docu.db_update()

	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 1 WHERE `field` = "allow_negative_stock" """)
	docu.update_stock_ledger()
	docu.make_gl_entries()
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 0 WHERE `field` = "allow_negative_stock" """)

@frappe.whitelist()
def execute_repair_gl_entry():
	repair_gl_entry("Purchase Receipt","BBKR-2023-03-00006")

@frappe.whitelist()
def repair_gl_entry(doctype,docname):
	
	docu = frappe.get_doc(doctype, docname)	
	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 1 WHERE `field` = "allow_negative_stock" """)
	docu.update_stock_ledger()
	docu.make_gl_entries()
	docu.repost_future_sle_and_gle()
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 0 WHERE `field` = "allow_negative_stock" """)
