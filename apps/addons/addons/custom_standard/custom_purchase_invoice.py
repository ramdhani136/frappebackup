# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe.model.naming import make_autoname

@frappe.whitelist()
def set_dimensi_item(doc,method):
	for row in doc.items:
		item = frappe.get_doc("Item",row.item_code)
		row.dimensi = item.dimensi

@frappe.whitelist()
def cek_image_item(doc,method):
	for row in doc.items:
		item = frappe.get_doc("Item",row.item_code)
		if not item.image:
			check = 1
			check_bypass = frappe.db.sql(""" SELECT value FROM `tabSingles` WHERE field = "approval_image_role" AND value IS NOT NULL """,as_dict = 1)
			check_role = ""
			if len(check_bypass) > 0:
				for row in check_bypass:
					check_role = row.value
			if check_role:
				if check_role in frappe.get_roles(frappe.session.user):
					check = 0

			if check == 1:
				frappe.throw("Image Item not set yet. Please check item {} - {}".format(item.item_code, item.item_name))
