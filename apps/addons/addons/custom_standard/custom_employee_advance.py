from __future__ import unicode_literals
import frappe
from frappe.utils import flt, comma_or, nowdate, getdate
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.status_updater import StatusUpdater

@frappe.whitelist()
def check_unfinished_advance(doc,method):
	check_unpaid = frappe.db.sql(""" SELECT name FROM `tabEmployee Advance` WHERE docstatus = 1 AND employee = "{}" AND advance_amount != claimed_amount + return_amount """.format(doc.employee))
	if len(check_unpaid) > 0:
		frappe.throw("There is unfinished Employee Advance linked to this Employee, ex. {} ".format(check_unpaid[0][0]))