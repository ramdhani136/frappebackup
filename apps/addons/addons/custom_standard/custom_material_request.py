# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# ERPNext - web based ERP (http://erpnext.com)
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import cstr, flt, getdate, new_line_sep, nowdate, add_days
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_indented_qty
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.stock.doctype.item.item import get_item_defaults

from six import string_types

@frappe.whitelist()
def custom_update_status(name, status):
	material_request = frappe.get_doc('Material Request', name)
	material_request.check_permission('write')
	material_request.workflow_state = "Closed"
	material_request.status = status
	material_request.db_update()

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		qty = flt(flt(obj.stock_qty) - flt(obj.ordered_qty))/ target.conversion_factor \
			if flt(obj.stock_qty) > flt(obj.ordered_qty) else 0
		target.qty = qty
		target.transfer_qty = qty * obj.conversion_factor
		target.conversion_factor = obj.conversion_factor

		if source_parent.material_request_type == "Material Transfer" or source_parent.material_request_type == "Customer Provided" or source_parent.material_request_type == "Material Receipt":
			target.t_warehouse = obj.warehouse
		else:
			target.s_warehouse = obj.warehouse

		if source_parent.material_request_type == "Customer Provided":
			target.allow_zero_valuation_rate = 1

	def set_missing_values(source, target):
		target.purpose = source.material_request_type
		if source.job_card:
			target.purpose = 'Material Transfer for Manufacture'

		if source.material_request_type == "Customer Provided":
			target.purpose = "Material Receipt"

		target.run_method("calculate_rate_and_amount")
		target.set_stock_entry_type()
		target.set_job_card_data()

	doclist = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["in", ["Material Transfer", "Material Issue", "Customer Provided"]]
			}
		},
		"Material Request Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"name": "material_request_item",
				"parent": "material_request",
				"uom": "stock_uom"
			},
			"postprocess": update_item,
			"condition": lambda doc: doc.ordered_qty < doc.stock_qty
		}
	}, target_doc, set_missing_values)

	return doclist