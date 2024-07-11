# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe.model.naming import make_autoname

@frappe.whitelist()
def bersih_bersih_ordered_qty(doc,method):
	for row in doc.items:
		row.ordered_qty = 0