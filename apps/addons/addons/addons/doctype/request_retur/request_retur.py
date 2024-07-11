# -*- coding: utf-8 -*-
# Copyright (c) 2021, PT DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RequestRetur(Document):
	
	def autoname(self):
		self.name = self.document_name


@frappe.whitelist()
def related_items(doctype, txt, searchfield, start, page_len, filters):
	list_item = frappe.db.sql("""SELECT item_code, item_name from `tab{} Item` where parent = "{}" """.format(filters.get("doctype"), filters.get("docname")))

	return list_item


@frappe.whitelist()
def make_sales_return(source_name, target_doc=None):
	from erpnext.controllers.sales_and_purchase_return import make_return_doc
	dt = frappe.db.get_value("Request Retur",source_name, "document_type")
	_rr = frappe.get_doc("Request Retur",source_name)
	items = _rr.items

	doc =  make_return_doc(dt, _rr.document_name, target_doc)

	array_item_code = []

	if doc.items:
		for item in doc.items:
			for _item in items:
				if item.item_code == _item.item_code:
					item.qty = _item.qty * -1
					array_item_code.append(item.item_code)

		# frappe.throw(str(array_item_code))
		baris_baris_item = []
		for item in doc.items:
			if item.item_code in array_item_code:
				baris_baris_item.append(item)

		doc.items = baris_baris_item
				
	return doc
