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
	if self.workflow_state == "Waiting Accounting" and self.overdue_invoices == 1:
		self.overdue_invoices = 0
		self.db_update()

@frappe.whitelist()
def check_overdue_invoice_with_field(self,method):
	controller = frappe.db.get_single_value("Accounts Settings","credit_controller")
	min_date = frappe.db.get_single_value("Overdue Settings","minimal_overdue_date")
	barrier = 1
	query_min = ""

	if min_date:
		query_min = """ AND due_date >= DATE("{}") """.format(min_date)
	if controller:
		if controller in frappe.get_roles(frappe.session.user):
			barrier = 1
			
	if barrier == 1:
		check_invoice = frappe.db.sql(""" 
			SELECT `name`,
			status,DATEDIFF(DATE(NOW()),due_date) as diff FROM `tabSales Invoice` WHERE
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
					self.overdue_invoices = 1

					over60=False
					for row in check_invoice:
						if list_invoice == "":
							list_invoice = row[0]
						else:
							list_invoice = list_invoice + "<br>" +  row[0]
						if cint(row[2])>=30:
							over60=True
					if over60:
						frappe.msgprint("Document can't be created <br/> customer {} has overdue invoice(s) that over 30 days, <br> {} ".format(self.customer, list_invoice)) 
					else:
						frappe.msgprint("Document created but customer {} has overdue invoice(s), <br> {} ".format(self.customer, list_invoice))



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
			barrier = 1

	if barrier == 1:
		check_invoice = frappe.db.sql(""" 
			SELECT `name`,
			status,DATEDIFF(DATE(NOW()),due_date) as diff FROM `tabSales Invoice` WHERE
			outstanding_amount > 0 AND 
			docstatus = 1 AND status != "Closed"
			and customer = "{}"
			AND due_date < DATE(NOW()) {} """.format(self.customer,query_min))

		customer = frappe.get_doc("Customer", self.customer)

		if customer.limit_customer_overdue != 0:
			if float(customer.limit_customer_overdue) > 0:

				limit_overdue = customer.limit_customer_overdue
				list_invoice = ""
				#if len(check_invoice) >= float(limit_overdue):
				over60=False
				for row in check_invoice:
					if list_invoice == "":
						list_invoice = row[0]
					else:
						list_invoice = list_invoice + "<br>" +  row[0]
					if cint(row[2])>=30:
						over60=True
				if over60:
					frappe.msgprint("Document can't be created <br/> customer {} has overdue invoice(s) that over 30 days, <br> {} ".format(self.customer, list_invoice)) 
				else:
					frappe.msgprint("Document created but customer {} has overdue invoice(s), <br> {} ".format(self.customer, list_invoice))
