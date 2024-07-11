# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from api_integration.validation import success_format, error_format

@frappe.whitelist(allow_guest=False)
def test():
	try:
		return success_format("SUCCESS")
	except:
		return error_format("ERROR")