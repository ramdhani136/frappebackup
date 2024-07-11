# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
#from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit,get_customer_outstanding,get_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from erpnext.stock.doctype.batch.batch import set_batch_nos

@frappe.whitelist()
def check_workflow_customer_limit(self,method):
	if (self.workflow_state == "Waiting Accounting" or self.docstatus == 1) and self.customer_limit == 1:
		self.customer_limit = 0
		self.db_update()

@frappe.whitelist()
def custom_method_submit(self,method):
	# self.validate_posting_time()
	# super(DeliveryNote, self).validate()
	if not self.is_return:
		custom_check_credit_limit(self)

def custom_validate(self):
	self.validate_posting_time()
	super(DeliveryNote, self).validate()

	if not self.is_return and not self.customer_limit:
		custom_check_credit_limit(self)

	self.set_status()
	self.so_required()
	self.validate_proj_cust()
	# custom chandra
	if not self.is_return:
		self.check_sales_order_on_hold_or_close("against_sales_order")

	self.validate_warehouse()
	self.validate_uom_is_integer("stock_uom", "stock_qty")
	self.validate_uom_is_integer("uom", "qty")
	self.validate_with_previous_doc()

	if self._action != 'submit' and not self.is_return:
		set_batch_nos(self, 'warehouse', True)

	from erpnext.stock.doctype.packed_item.packed_item import make_packing_list
	make_packing_list(self)

	self.update_current_stock()

	if not self.installation_status: self.installation_status = 'Not Installed'

def custom_check_credit_limit(self):
	from erpnext.selling.doctype.customer.customer import check_credit_limit

	extra_amount = 0
	validate_against_credit_limit = False
	bypass_credit_limit_check_at_sales_order = cint(frappe.db.get_value("Customer Credit Limit",
		filters={'parent': self.customer, 'parenttype': 'Customer', 'company': self.company},
		fieldname="bypass_credit_limit_check"))

	if bypass_credit_limit_check_at_sales_order:
		validate_against_credit_limit = True
		extra_amount = self.base_grand_total
	else:
		for d in self.get("items"):
			if not (d.against_sales_order or d.against_sales_invoice):
				validate_against_credit_limit = True
				break

	if validate_against_credit_limit:
		check = custom_customer_check_credit_limit(self.customer, self.company,
			bypass_credit_limit_check_at_sales_order, extra_amount,self.workflow_state!="Draft")

		if check == 1:
			self.customer_limit = 1
		else:
			self.customer_limit = 0

DeliveryNote.validate = custom_validate

def custom_customer_check_credit_limit(customer, company, ignore_outstanding_sales_order=False, extra_amount=0,block=False):
	customer_outstanding = get_customer_outstanding(customer, company, ignore_outstanding_sales_order)
	if extra_amount > 0:
		customer_outstanding += flt(extra_amount)

	credit_limit = get_credit_limit(customer, company)
	if credit_limit > 0 and flt(customer_outstanding) > credit_limit:
		frappe.msgprint(_("Credit limit has been crossed for customer {0} ({1}/{2})")
			.format(customer, customer_outstanding, credit_limit))

		# If not authorized person raise exception
		credit_controller = frappe.db.get_value('Accounts Settings', None, 'credit_controller')
		if not credit_controller or credit_controller not in frappe.get_roles():
			frappe.msgprint(_("Please contact to the user who have Sales Master Manager {0} role").format(" / " + credit_controller if credit_controller else ""))

		return 1

	return 0


def custom_update_reserved_qty(self):
	so_map = {}
	for d in self.get("items"):
		if d.so_detail:
			if self.doctype == "Delivery Note" and d.against_sales_order:
				so_map.setdefault(d.against_sales_order, []).append(d.so_detail)
			elif self.doctype == "Sales Invoice" and d.sales_order and self.update_stock:
				so_map.setdefault(d.sales_order, []).append(d.so_detail)

	for so, so_item_rows in so_map.items():
		if so and so_item_rows:
			sales_order = frappe.get_doc("Sales Order", so)
			if not self.get("is_return"):
				if sales_order.status in ["Closed", "Cancelled"]:
					frappe.throw(_("{0} {1} is cancelled or closed").format(_("Sales Order"), so),
						frappe.InvalidStatusError)

			sales_order.update_reserved_qty(so_item_rows)

SellingController.update_reserved_qty = custom_update_reserved_qty

@frappe.whitelist()
def custom_method_validate(doc,method):
	# frappe.msgprint("wkwkwkw2")
	if doc.is_return == 0:
		for row in doc.items:
			if row.against_sales_order:
				so = frappe.get_doc("Sales Order",row.against_sales_order)
				if so.workflow_state!="Approved":
					frappe.throw("Sales Order {} is not Approved Yet".format(row.against_sales_order))

	DeliveryNote.validate = custom_validate
	SellingController.update_reserved_qty = custom_update_reserved_qty

	# for i in doc.items:
	# 	# frappe.throw(i.item_code)
	# 	if i.batal_kirim == 1:
	# 		frappe.throw("Item "+i.item_code+" Melakukan batal Kirim silahkan hapus terlebih dahulu untuk melanjutkan !")

@frappe.whitelist()
def custom_make_delivery_note(source_name, target_doc=None, skip_item_mapping=False):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({'company_address': source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
		target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		target.qty = flt(source.qty) - flt(source.delivered_qty)
		target.qty_ordered = flt(source.qty) - flt(source.delivered_qty)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)

		if item:
			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
				or item.get("buying_cost_center") \
				or item_group.get("buying_cost_center")

	mapper = {
		"Sales Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}

	if not skip_item_mapping:
		mapper["Sales Order Item"] = {
			"doctype": "Delivery Note Item",
			"field_map": {
				"rate": "rate",
				"name": "so_detail",
				"parent": "against_sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		}

	target_doc = get_mapped_doc("Sales Order", source_name, mapper, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def get_confirmation_doc(doc,method):
	# print("wkwkwkwkw")
	# frappe.msgprint("kk2")
	pass
	# if frappe.local.site == 'etmsdadev.digitalasiasolusindo.com':
	# 	frappe.msgprint("ss")
	# 	if doc.confirmation_document:
	# 		data = frappe.db.sql(""" SELECT cd.name,cd.qty_muat,cd.sumber_document,cd.sumber_document_name 
	# 			from `tabConfirmation Document Item` cd where cd.parent = '{}' """.format(doc.confirmation_document),as_dict=1)

	# 		if data:
	# 			for i in data:
	# 				frappe.db.sql(""" UPDATE `tabDelivery Note Item` set qty_confirmation_doc = {} where name = '{}' and parent='{}' """.format(i['qty_muat'],i['sumber_document'],i['sumber_document_name']),debug=1)
	# 				frappe.db.commit()

	# 		for d in doc.items:
	# 			if d.qty_confirmation_doc != 0:
	# 				d.qty = d.qty_tambahan + d.qty_confirmation_doc