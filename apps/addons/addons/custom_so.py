# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import now, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from datetime import datetime

from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, getdate, cint, cstr, get_formatted_email, today
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc

from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

from erpnext.selling.doctype.customer.customer import get_credit_limit,get_customer_outstanding
from frappe.utils.user import get_users_with_role

@frappe.whitelist()
def custom_on_submit(self):
	custom_check_credit_limit(self.customer, self.company)
	self.update_reserved_qty()

	frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype, self.company, self.base_grand_total, self)
	self.update_project()
	self.update_prevdoc_status('submit')

	self.update_blanket_order()

	update_linked_doc(self.doctype, self.name, self.inter_company_order_reference)
	if self.coupon_code:
		from erpnext.accounts.doctype.pricing_rule.utils import update_coupon_code_count
		update_coupon_code_count(self.coupon_code,'used')

SalesOrder.on_submit = custom_on_submit

@frappe.whitelist()
def override_check_credit_limit(self,method):
	SalesOrder.on_submit = custom_on_submit

@frappe.whitelist()
def custom_on_insert(self,method):
	custom_check_credit_limit(self.customer, self.company)

def custom_check_credit_limit(customer, company, ignore_outstanding_sales_order=False, extra_amount=0,block=False):
	credit_limit = get_credit_limit(customer, company)
	if not credit_limit:
		return

	customer_outstanding = get_customer_outstanding(customer, company, ignore_outstanding_sales_order)
	if extra_amount > 0:
		customer_outstanding += flt(extra_amount)

	if credit_limit > 0 and flt(customer_outstanding) > credit_limit:
		frappe.msgprint(
			_("Credit limit has been crossed for customer {0} ({1}/{2})").format(
				customer, customer_outstanding, credit_limit
			)
		)

		# If not authorized person raise exception
		credit_controller_role = frappe.db.get_single_value("Accounts Settings", "credit_controller")
		if not credit_controller_role or credit_controller_role not in frappe.get_roles():
			# form a list of emails for the credit controller users
			credit_controller_users = get_users_with_role(credit_controller_role or "Sales Master Manager")

			# form a list of emails and names to show to the user
			credit_controller_users_formatted = [
				get_formatted_email(user).replace("<", "(").replace(">", ")")
				for user in credit_controller_users
			]
			if not credit_controller_users_formatted:
				if block:
					frappe.throw(
						_("Please contact your administrator to extend the credit limits for {0}.").format(customer)
					)

			message = """Please contact any of the following users to extend the credit limits for {0}:
				<br><br><ul><li>{1}</li></ul>""".format(
				customer, "<li>".join(credit_controller_users_formatted)
			)

			# if the current user does not have permissions to override credit limit,
			# prompt them to send out an email to the controller users
			frappe.msgprint(
				message,
				title="Notify",
				raise_exception=0,
				primary_action={
					"label": "Send Email",
					"server_action": "erpnext.selling.doctype.customer.customer.send_emails",
					"args": {
						"customer": customer,
						"customer_outstanding": customer_outstanding,
						"credit_limit": credit_limit,
						"credit_controller_users_list": credit_controller_users,
					},
				},
			)


@frappe.whitelist()
def net_stock_available(self,method):
	for row in self.items:
		if row.actual_qty or row.projected_qty:
			row.net_stock_available = flt(row.actual_qty) - flt(row.projected_qty)
			row.db_update()

def set_bottom_price(doc,method):
	for item in doc.items:
		btm_pricelist = frappe.db.get_single_value("Selling Settings","minimum_price_list")
		bottom_price = frappe.db.get_value("Item Price", {"item_code":item.item_code,"price_list":btm_pricelist,"selling":1,"uom":item.stock_uom},"price_list_rate")
		if not bottom_price:
			bottom_price = 0
		
		frappe.db.set_value("Sales Order Item",item.name, "minimum_price_hint",bottom_price)

@frappe.whitelist()
def custom_set_status_all():
	list_invoice = frappe.db.sql(""" SELECT name FROM `tabSales Invoice` WHERE outstanding_amount > 0 AND docstatus = 1 """)
	for row in list_invoice:
		self = frappe.get_doc("Sales Invoice", row[0])
		self.set_status()
		self.db_update()

@frappe.whitelist()
def custom_set_status(self,method):
	self.set_status()
	self.db_update()


@frappe.whitelist()
def check_customer_group(doc,method):
	customer_doc = frappe.get_doc("Customer",doc.customer)
	doc.customer_group = customer_doc.customer_group
	doc.db_update()

@frappe.whitelist()
def check_overdue_invoice(self,method):

	controller = frappe.db.get_single_value("Accounts Settings","credit_controller")
	if controller:
		if controller not in frappe.get_roles(frappe.session.user):
			check_invoice = frappe.db.sql(""" 
				SELECT `name`,
				status,due_date,DATE(NOW()) FROM `tabSales Invoice` WHERE
				outstanding_amount > 0 AND 
				docstatus = 1 AND status != "Closed"
				and customer = "{}"
				AND due_date < DATE(NOW()) """.format(self.customer))

			customer = frappe.get_doc("Customer", self.customer)

			if customer.limit_customer_overdue != 0:
				if float(customer.limit_customer_overdue) > 0:
					limit_overdue = customer.limit_customer_overdue
					list_invoice = ""
					if len(check_invoice) >= float(limit_overdue):
						for row in check_invoice:
							if list_invoice == "":
								list_invoice = row[0]
							else:
								list_invoice = list_invoice + "<br>" +  row[0]

						frappe.throw("Document can't be created as long customer {} has overdue invoice(s), e.g. <br> {} ".format(self.customer, list_invoice)) 

@frappe.whitelist()
def set_close_so(self,method):
	if self.workflow_state == "Closed":
		self.update_status("Closed")
	else:
		self.update_status("Draft")

@frappe.whitelist()
def set_ste_dll(self,method):
	if not self.dibuat_oleh:
		self.dibuat_oleh = frappe.get_doc("User",self.owner).full_name
		self.dibuat_oleh_datetime = self.creation
		self.diapprove_oleh = frappe.get_doc("User",frappe.session.user).full_name
		if self.doctype != "Request Retur":
			tmp = self.workflow_state
			self.workflow_state = tmp
		
		self.diapprove_oleh_datetime = now()
		#self.db_update()

@frappe.whitelist()
def set_sales_dll(self,method):
	if self.workflow_state == "In Inventory Control":
		if not self.sales:
			self.sales = frappe.get_doc("User",frappe.session.user).full_name
			self.datetime_sales = now()
			self.db_update()

	elif self.workflow_state == "In Purchasing" or self.workflow_state == "Waiting Confirmation":
		if not self.dic:	
			self.dic = frappe.get_doc("User",frappe.session.user).full_name
			self.datetime_dic = now()
			self.db_update()

	elif self.workflow_state == "Approved":
		if not self.koordinator:
			self.koordinator = frappe.get_doc("User",frappe.session.user).full_name
			self.datetime_koordinator = now()
			self.db_update()

	elif self.workflow_state == "Pending Sales Confirmation":
		if not self.purchasing:
			self.purchasing = frappe.get_doc("User",frappe.session.user).full_name
			
			self.datetime_purchasing = now()
			self.db_update()
	elif self.workflow_state == "Closed":
		self.update_status("Closed")

@frappe.whitelist()
def set_purchase_invoice_dll(self,method):
	if self.workflow_state == "Waiting Confirmation":
		if not self.dibuat_oleh:
			self.dibuat_oleh = frappe.get_doc("User",frappe.session.user).full_name
			
			self.datetime_dibuat_oleh = now()
			self.db_update()

	elif self.workflow_state == "Approved by Purchasing":
		if not self.diketahui_oleh:	
			self.diketahui_oleh = frappe.get_doc("User",frappe.session.user).full_name
			
			self.diketahui_oleh_datetime = now()
			self.db_update()

	elif self.workflow_state == "Approved":
		if not self.diapprove_oleh:
			self.diapprove_oleh = frappe.get_doc("User",frappe.session.user).full_name
			
			self.diapprove_oleh_datetime = now()
			self.db_update()


@frappe.whitelist()
def set_purchase_dll(self,method):
	if self.workflow_state == "Waiting Confirmation":
		if not self.dibuat_oleh:
			self.dibuat_oleh = frappe.get_doc("User",frappe.session.user).full_name
			
			self.datetime_dibuat_oleh = now()
			self.db_update()

	elif self.workflow_state == "Approved by Purchasing":
		if not self.mengetahui:	
			self.mengetahui = frappe.get_doc("User",frappe.session.user).full_name
			
			self.datetime_mengetahui = now()
			self.db_update()

	elif self.workflow_state == "Approved":
		# tambahan andy agar qty PO update ke Bin
		self.update_status("Submitted")
		# end andy	
		if not self.menyetujui:
			self.menyetujui = frappe.get_doc("User",frappe.session.user).full_name
			
			self.datetime_menyetujui = now()
			self.db_update()

	# tambahan andy agar qty PO update ke Bin
	elif self.workflow_state == "Closed":
		self.update_status("Closed")


@frappe.whitelist()
def set_journal_dll(self,method):
	if self.workflow_state == "Waiting Confirmation":
		if not self.mengetahui:
			self.mengetahui = frappe.get_doc("User",frappe.session.user).full_name
			
			self.mengetahui_datetime = now()
			self.db_update()

	elif self.workflow_state == "Approved":
		if not self.diperiksa:
			self.diperiksa = frappe.get_doc("User",frappe.session.user).full_name
			
			self.diperiksa_datetime = now()
			self.db_update()


@frappe.whitelist()
def set_payment_dll(self,method):
	if self.workflow_state == "Waiting Confirmation":
		if not self.mengetahui:
			self.mengetahui = frappe.get_doc("User",frappe.session.user).full_name
			
			self.mengetahui_datetime = now()
			self.db_update()

	elif self.workflow_state == "Approved":
		if not self.diperiksa:
			self.diperiksa = frappe.get_doc("User",frappe.session.user).full_name
			
			self.diperiksa_datetime = now()
			self.db_update()

@frappe.whitelist()
def autoname_so(doc,method):
	if doc.manual_naming:
		doc.name = doc.manual_naming
	else:
		patokan_naming_series = doc.naming_series
		yy = str(doc.transaction_date).split("-")[0][-4:]
		mm = str(doc.transaction_date).split("-")[1]
		dd = str(doc.transaction_date).split("-")[2]
		naming_series = doc.naming_series.replace(".YYYY.",yy).replace(".MM.",mm)
		check_series = frappe.db.sql(""" SELECT current FROM `tabSeries` WHERE name = "Current {}" """.format(naming_series))
		po_sekarang = "Current " + str(naming_series)
		check_number = 0

		if len(check_series) > 0:
			check_number = int(check_series[0][0])
			check_sales_order = 0
			while check_sales_order == 0:
				check = frappe.db.sql(""" SELECT name FROM `tabSales Order` WHERE name = '{}' """.format(naming_series.replace(".####.", str(check_number).zfill(4))))
				if len(check) > 0:
					check_number += 1
				else:
					check_sales_order = 1
			frappe.db.sql("update tabSeries set current = current+1 where name=%s", (po_sekarang))
		else:
			check_number = 1
			check_sales_order = 0
			while check_sales_order == 0:
				check = frappe.db.sql(""" SELECT name FROM `tabSales Order` WHERE name = '{}' """.format(naming_series.replace(".####.", str(check_number).zfill(4))))
				if len(check) > 0:
					check_number += 1
				else:
					check_sales_order = 1
					
			frappe.db.sql(""" insert into tabSeries (name, current) values ("{}", {} ) """.format(po_sekarang, check_number))
			
		naming_series = naming_series.replace(".####.", str(check_number).zfill(4))
		doc.name = naming_series

@frappe.whitelist()
def autoname_sinv(doc,method):
	if doc.manual_naming:
		doc.name = doc.manual_naming

@frappe.whitelist()
def query_ekspedisi(doctype, txt, searchfield, start, page_len, filters ):

	# frappe.throw("""
	# 		SELECT tet.ekspedisi FROM `tabEkspedisi` te JOIN `tabEkspedisi Table` tet ON tet.`ekspedisi` = te.`name`
	# 		JOIN `tabCustomer` tc ON tc.name = tet.`parent`

	# 		WHERE tc.name = "{customer}" 
	# 		and tet.ekspedisi like %(txt)s
	# 	""".format(
	# 		customer =filters.get("customer"),
	# 		start=start,
	# 		page_len=page_len), {
	# 			"txt": "%{0}%".format(txt),
	# 			"_txt": txt.replace('%', '')
	# 		})

	return frappe.db.sql("""
			SELECT tet.ekspedisi FROM `tabEkspedisi` te JOIN `tabEkspedisi Table` tet ON tet.`ekspedisi` = te.`name`
			JOIN `tabCustomer` tc ON tc.name = tet.`parent`

			WHERE tc.name = "{customer}" 
			and tet.ekspedisi like %(txt)s
		""".format(
			customer =filters.get("customer"),
			start=start,
			page_len=page_len), {
				"txt": "%{0}%".format(txt),
				"_txt": txt.replace('%', '')
			})

# edited rico 19 april 2021
@frappe.whitelist()
def cek_qty_so_dengan_qty_qtn(doc,method):
	# ordered_qty

	# submit
	if doc.docstatus == 0 :
		for i in doc.items :
			if i.prevdoc_docname :
				if i.prevdoc_detail :
					# cek dengan ordered_qty
					get_qtni = frappe.db.sql(""" SELECT qtni.`name`, qtni.`item_code`, qtni.`stock_qty`, IFNULL(qtni.`ordered_qty`, 0) 
						FROM `tabQuotation Item` qtni WHERE qtni.`parent` = "{}" AND qtni.`name` = "{}" """.format(i.prevdoc_docname, i.prevdoc_detail))

					item_stock_qty = 0
					item_ordered_qty = 0
					if get_qtni :
						if get_qtni[0][2] :
							item_stock_qty = get_qtni[0][2]

						if get_qtni[0][3] :
							item_ordered_qty = get_qtni[0][3]

						# kalau qty nya yang di order lebih besar dari qty QTN
						if item_stock_qty < (i.stock_qty + item_ordered_qty) :
							frappe.throw("Qty untuk item "+str(i.item_code)+" pada baris "+str(i.idx)+" melebihin Qty yang ada di Quotation "+str(i.prevdoc_docname))


						# kalau tidak melebihi
						item_ordered_qty = item_ordered_qty + i.stock_qty
						# update qtni ordered_qty
						frappe.db.sql(""" UPDATE `tabQuotation Item` qtni SET qtni.`ordered_qty` = "{}" WHERE qtni.`parent` = "{}" AND qtni.`name` = "{}" """.format(item_ordered_qty, i.prevdoc_docname, i.prevdoc_detail))
						frappe.db.commit()



	# cancel
	elif doc.docstatus == 2 :
		for i in doc.items :
			if i.prevdoc_docname :
				if i.prevdoc_detail :
					# cek dengan ordered_qty
					get_qtni = frappe.db.sql(""" SELECT qtni.`name`, qtni.`item_code`, qtni.`stock_qty`, IFNULL(qtni.`ordered_qty`, 0) 
						FROM `tabQuotation Item` qtni WHERE qtni.`parent` = "{}" AND qtni.`name` = "{}" """.format(i.prevdoc_docname, i.prevdoc_detail))

					item_stock_qty = 0
					item_ordered_qty = 0
					if get_qtni :
						if get_qtni[0][2] :
							item_stock_qty = get_qtni[0][2]

						if get_qtni[0][3] :
							item_ordered_qty = get_qtni[0][3]

						# kalau tidak melebihi
						item_ordered_qty = item_ordered_qty - i.stock_qty
						# update qtni ordered_qty
						frappe.db.sql(""" UPDATE `tabQuotation Item` qtni SET qtni.`ordered_qty` = "{}" WHERE qtni.`parent` = "{}" AND qtni.`name` = "{}" """.format(item_ordered_qty, i.prevdoc_docname, i.prevdoc_detail))
						frappe.db.commit()




# ============= edited rico 19 april override function =================

@frappe.whitelist()
def custom_make_sales_order(source_name, target_doc=None):
	quotation = frappe.db.get_value("Quotation", source_name, ["transaction_date", "valid_till"], as_dict = 1)
	if quotation.valid_till and (quotation.valid_till < quotation.transaction_date or quotation.valid_till < getdate(nowdate())):
		frappe.throw(_("Validity period of this quotation has ended."))
	return _custom_make_sales_order(source_name, target_doc)

def _custom_make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	customer = _custom_make_customer(source_name, ignore_permissions)

	def set_missing_values(source, target):
		if customer:
			target.customer = customer.name
			target.customer_name = customer.customer_name
		if source.referral_sales_partner:
			target.sales_partner=source.referral_sales_partner
			target.commission_rate=frappe.get_value('Sales Partner', source.referral_sales_partner, 'commission_rate')
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = ignore_permissions
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(obj, target, source_parent):
		# edited rico 19 april 2021
		# target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)
		target.stock_qty = (flt(obj.qty) - obj.ordered_qty) * flt(obj.conversion_factor)
		target.qty = (flt(obj.qty) - obj.ordered_qty)
		# target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)

		# if obj.against_blanket_order:
		# 	target.against_blanket_order = obj.against_blanket_order
		# 	target.blanket_order = obj.blanket_order
		# 	target.blanket_order_rate = obj.blanket_order_rate

	doclist = get_mapped_doc("Quotation", source_name, {
			"Quotation": {
				"doctype": "Sales Order",
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Quotation Item": {
				"doctype": "Sales Order Item",
				"field_map": {
					"parent": "prevdoc_docname",
					"name" : "prevdoc_detail"
				},
				"postprocess": update_item,
				"condition": lambda doc: (doc.qty - doc.ordered_qty) > 0
			},
			"Sales Taxes and Charges": {
				"doctype": "Sales Taxes and Charges",
				"add_if_empty": True
			},
			"Sales Team": {
				"doctype": "Sales Team",
				"add_if_empty": True
			},
			"Payment Schedule": {
				"doctype": "Payment Schedule",
				"add_if_empty": True
			}
		}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	# postprocess: fetch shipping address, set missing values
	doclist.set_onload("ignore_price_list", True)

	return doclist

def _custom_make_customer(source_name, ignore_permissions=False):
	quotation = frappe.db.get_value("Quotation",
		source_name, ["order_type", "party_name", "customer_name"], as_dict=1)

	if quotation and quotation.get('party_name'):
		if not frappe.db.exists("Customer", quotation.get("party_name")):
			lead_name = quotation.get("party_name")
			customer_name = frappe.db.get_value("Customer", {"lead_name": lead_name},
				["name", "customer_name"], as_dict=True)
			if not customer_name:
				from erpnext.crm.doctype.lead.lead import _make_customer
				customer_doclist = _make_customer(lead_name, ignore_permissions=ignore_permissions)
				customer = frappe.get_doc(customer_doclist)
				customer.flags.ignore_permissions = ignore_permissions
				if quotation.get("party_name") == "Shopping Cart":
					customer.customer_group = frappe.db.get_value("Shopping Cart Settings", None,
						"default_customer_group")

				try:
					customer.insert()
					return customer
				except frappe.NameError:
					if frappe.defaults.get_global_default('cust_master_name') == "Customer Name":
						customer.run_method("autoname")
						customer.name += "-" + lead_name
						customer.insert()
						return customer
					else:
						raise
				except frappe.MandatoryError as e:
					mandatory_fields = e.args[0].split(':')[1].split(',')
					mandatory_fields = [customer.meta.get_label(field.strip()) for field in mandatory_fields]

					frappe.local.message_log = []
					lead_link = frappe.utils.get_link_to_form("Lead", lead_name)
					message = _("Could not auto create Customer due to the following missing mandatory field(s):") + "<br>"
					message += "<br><ul><li>" + "</li><li>".join(mandatory_fields) + "</li></ul>"
					message += _("Please create Customer from Lead {0}.").format(lead_link)

					frappe.throw(message, title=_("Mandatory Missing"))
			else:
				return customer_name
		else:
			return frappe.get_doc("Customer", quotation.get("party_name"))


# =============================================
