from __future__ import unicode_literals
import frappe
import math
from frappe import _

#def dn_autoname(self, method):
#    frappe.msgprint('Tes')
def patch_account():
	data=frappe.db.sql("""select income_account,parent,expense_account from `tabItem Default` where parenttype="Item Group" """,as_list=1)
	for row in data:
		if row[0]:
			frappe.db.sql("""update `tabSales Invoice Item` set income_account="{}" where item_group="{}" """.format(row[0],row[1]))
		if row[2]:
			frappe.db.sql("""update `tabDelivery Note Item` set expense_account="{}" where item_group="{}" """.format(row[2],row[1]))
def patch_data():
	doctype="Sales Invoice"
	docname="SJ-2022-09-00199"
	docu = frappe.get_doc(doctype, docname)
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	docu.make_gl_entries()
	frappe.db.commit()
