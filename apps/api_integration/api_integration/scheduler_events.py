# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

def remove_success_api():
	try:
		frappe.db.sql("""
			DELETE FROM `tabAPI Log`
			WHERE status_code = 200
			""")
		frappe.db.commit()
	except:
		frappe.log_error(frappe.get_traceback(), "ERROR: Scheduler Events Remove Success API")