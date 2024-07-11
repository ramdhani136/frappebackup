# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from datetime import datetime

from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, getdate
from frappe import _

@frappe.whitelist()
def check_workflow_invoice_overdues(self,method):
	if (self.workflow_state == "Waiting Accounting" or self.docstatus == 1) and self.overdue_invoices == 1:
		self.overdue_invoices = 0
		self.db_update()


@frappe.whitelist()
def check_overdue_invoice(self,method):

	controller = frappe.db.get_single_value("Accounts Settings","credit_controller")
	min_date = frappe.db.get_single_value("Overdue Settings","minimal_overdue_date")
	barrier = 1
	query_min = ""
	if min_date:
		query_min = """ AND due_date >= DATE("{}") """.format(min_date)
	if controller:
		if controller in frappe.get_roles(frappe.session.user):
			barrier = 0

	if barrier == 1:
		check_invoice = frappe.db.sql(""" 
			SELECT `name`,
			status,due_date,DATE(NOW()) FROM `tabSales Invoice` WHERE
			outstanding_amount > 0 AND 
			docstatus = 1 AND status != "Closed"
			and customer = "{}"
			AND due_date < DATE(NOW()) {} """.format(self.customer,query_min))

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

