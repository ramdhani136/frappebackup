# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.item.item import get_item_defaults



def update_item(obj, target, source_parent):
	target.conversion_factor = obj.conversion_factor
	target.qty = flt(flt(obj.stock_qty) - flt(obj.ordered_qty))/ target.conversion_factor
	target.stock_qty = (target.qty * target.conversion_factor)
	if getdate(target.schedule_date) < getdate(nowdate()):
		target.schedule_date = None
		
def set_missing_values(source, target_doc):
	if target_doc.doctype == "Purchase Order" and getdate(target_doc.schedule_date) <  getdate(nowdate()):
		target_doc.schedule_date = None
	target_doc.run_method("set_missing_values")
	target_doc.run_method("calculate_taxes_and_totals")

@frappe.whitelist()
def custom_make_purchase_order(source_name, target_doc=None):

	def postprocess(source, target_doc):
		if frappe.flags.args and frappe.flags.args.default_supplier:
			# items only for given default supplier
			supplier_items = []
			for d in target_doc.items:
				default_supplier = get_item_defaults(d.item_code, target_doc.company).get('default_supplier')
				if frappe.flags.args.default_supplier == default_supplier:
					supplier_items.append(d)
			target_doc.items = supplier_items

		set_missing_values(source, target_doc)

	def select_item(d):
		return d.ordered_qty < d.stock_qty

	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			}
		},
		"Material Request Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["uom", "stock_uom"],
				["uom", "uom"],
				["sales_order", "sales_order"],
				["sales_order_item", "sales_order_item"]
			],
			"postprocess": update_item,
			"condition": select_item
		}
	}, target_doc, postprocess)
	for row in doclist.items:
		if row.item_code and doclist.buying_price_list and doclist.supplier:
			args = {
				"item_code" : row.item_code,
				"price_list": doclist.buying_price_list,
				"supplier" : doclist.supplier,
				"uom" : row.uom,
				"transaction_date" : doclist.transaction_date,
				"doctype": doclist.doctype
			}
			
			conditions = """where item_code=%(item_code)s
				and price_list=%(price_list)s
				and ifnull(uom, '') in ('', %(uom)s)"""

			if args.get("customer") and "Purchase" not in args.get("doctype"):
				conditions += " and customer=%(customer)s"
			elif args.get("supplier"):
				conditions += " and supplier=%(supplier)s"
			else:
				conditions += "and (customer is null or customer = '') and (supplier is null or supplier = '')"

			if args.get('transaction_date'):
				conditions += """ and %(transaction_date)s between
					ifnull(valid_from, '2000-01-01') and ifnull(valid_upto, '2500-12-31')"""

			price_list_rate =  frappe.db.sql(""" select name, price_list_rate, uom
				from `tabItem Price` {conditions}
				order by valid_from desc, uom desc """.format(conditions=conditions), args)

			if price_list_rate:
				if price_list_rate[0]:
					if price_list_rate[0][1]:
						row.rate = price_list_rate[0][1]


		doclist.run_method("calculate_taxes_and_totals")

	return doclist

@frappe.whitelist()
def check_price_list(doc,method):
	for row in doc.items:
		args = {
			"item_code" : row.item_code,
			"price_list": doc.buying_price_list,
			"supplier" : doc.supplier,
			"uom" : row.uom,
			"transaction_date" : doc.transaction_date,
			"doctype": doc.doctype
		}
		
		conditions = """where item_code=%(item_code)s
			and price_list=%(price_list)s
			and ifnull(uom, '') in ('', %(uom)s)"""

		if args.get("customer") and "Purchase" not in args.get("doctype"):
			conditions += " and customer=%(customer)s"
		elif args.get("supplier"):
			conditions += " and supplier=%(supplier)s"
		else:
			conditions += "and (customer is null or customer = '') and (supplier is null or supplier = '')"

		if args.get('transaction_date'):
			conditions += """ and %(transaction_date)s between
				ifnull(valid_from, '2000-01-01') and ifnull(valid_upto, '2500-12-31')"""

		price_list_rate =  frappe.db.sql(""" select name, price_list_rate, uom
			from `tabItem Price` {conditions}
			order by valid_from desc, uom desc """.format(conditions=conditions), args)

		if price_list_rate:
			if price_list_rate[0]:
				if price_list_rate[0][1]:
					row.rate = price_list_rate[0][1]

@frappe.whitelist()
def check_received_po(doc,method):
	# frappe.throw("ASD")
	if not doc.is_new():
		frappe.db.sql(""" UPDATE `tabPurchase Order Item` SET received_qty = 0 WHERE parent = "{}" """.format(doc.name))
		check_pr = frappe.db.sql(""" SELECT parent FROM `tabPurchase Receipt Item` WHERE purchase_order = "{}" AND docstatus = 1 GROUP BY parent """.format(doc.name))
		for row in check_pr:
			pr_doc=frappe.get_doc("Purchase Receipt",row[0])
			pr_doc.update_prevdoc_status()
		frappe.db.commit()
		
		for row in doc.items:
			# row.received_qty = 0
			recd_qty = 0
			check = frappe.db.sql(""" SELECT received_qty FROM `tabPurchase Receipt Item` tpi WHERE name = "{}" """.format(row.name))
			if len(check) > 0:
				recd_qty = check[0][0]

			row.received_qty = recd_qty

@frappe.whitelist()
def manual_check_received_po():
	doc = frappe.get_doc("Purchase Order","PO-2021-02-00038")
	frappe.db.sql(""" UPDATE `tabPurchase Order Item` SET received_qty = 0 WHERE parent = "{}" """.format(doc.name))
	check_pr = frappe.db.sql(""" SELECT parent FROM `tabPurchase Receipt Item` WHERE purchase_order = "{}" AND docstatus = 1 GROUP BY parent """.format(doc.name))
	for row in check_pr:
		pr_doc=frappe.get_doc("Purchase Receipt",row[0])
		pr_doc.update_prevdoc_status()

@frappe.whitelist()
def autoname_po(doc,method):
	if "PO-.YYYY.-.MM.-.#####.P" in doc.naming_series:
		yy = str(doc.transaction_date).split("-")[0][-4:]
		mm = str(doc.transaction_date).split("-")[1]
		dd = str(doc.transaction_date).split("-")[2]
		naming_series = doc.naming_series.replace(".YYYY.",yy).replace(".MM.",mm)
		check_series = frappe.db.sql(""" SELECT current FROM `tabSeries` WHERE name = "Current PO-{}-{}-P" """.format(yy,mm))
		po_sekarang = "Current PO-{}-{}-P".format(yy,mm)
		check_number = 0
		if yy == "2021":
			if mm == "1":
				return

		if len(check_series) > 0:
			check_number = int(check_series[0][0])
			frappe.db.sql("update tabSeries set current = current+1 where name=%s", (po_sekarang))
		else:
			check_number = 1
			frappe.db.sql("insert into tabSeries (name, current) values (%s, 1)", (po_sekarang))
			
		naming_series = naming_series.replace(".#####.", str(check_number).zfill(5))
		doc.name = naming_series