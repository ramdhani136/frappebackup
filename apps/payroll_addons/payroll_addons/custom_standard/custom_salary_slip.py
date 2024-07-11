# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, flt, nowdate, add_days, getdate, fmt_money, add_to_date, DATE_FORMAT, date_diff
from frappe import _
from erpnext.accounts.utils import get_fiscal_year
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
import json 
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry


@frappe.whitelist()
def check_keterangan(self,method):
	for row in self.earnings:
		if row.salary_component:
			check = frappe.db.sql(""" 
				SELECT component FROM `tabComponent Detail`
				WHERE component = "{}" """.format(row.salary_component))
			if len(check) > 0:
				if not row.keterangan:
					frappe.throw("Keterangan diwajibkan untuk komponen {} di Salary Slip {} ".format(row.salary_component,self.name))
		

