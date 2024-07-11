# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe.model.naming import make_autoname

@frappe.whitelist()
def check_expense(doc,method):
	if doc.stock_entry_type == "Manufacture":
		if doc.company:
			com = frappe.get_doc("Company", doc.company)
			if com.expense_account_for_manufacture:
				for row in doc.items:
					if str(row.expense_account) != str(com.expense_account_for_manufacture):
						row.expense_account = com.expense_account_for_manufacture

@frappe.whitelist()
def patch_ste():
	query = frappe.db.sql(""" SELECT sted.parent 
			FROM `tabStock Entry Detail` sted
			JOIN `tabStock Entry` ste
			ON sted.parent = ste.name
			WHERE `expense_account` != "5300.002 - Koreksi Selisih Stock - ETM-BGR"
			AND ste.`purpose` = "Manufacture"
			AND ste.`docstatus` = 1
			GROUP BY sted.parent """)
	for row in query:
		ste = frappe.get_doc("Stock Entry", row[0])
		print(ste.name)
		check = 0
		com = frappe.get_doc("Company", ste.company)
		if com.expense_account_for_manufacture:
			for row_item in ste.items:
				if str(row_item.expense_account) != str(com.expense_account_for_manufacture):
					row_item.expense_account = com.expense_account_for_manufacture
					check = 1
					row_item.db_update()

		if check == 1:
			delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(ste.name))
			delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(ste.name))
			ste.update_stock_ledger()
			ste.make_gl_entries()
			# print("Membenarkan LEDGER dari {} - DONE ".format(docname))
			frappe.db.commit()