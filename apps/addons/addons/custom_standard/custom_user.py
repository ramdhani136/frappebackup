# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe
from frappe.model.document import Document
from frappe.utils import cint, flt, has_gravatar, escape_html, format_datetime, now_datetime, get_formatted_email, today
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.desk.doctype.notification_settings.notification_settings import create_notification_settings
from frappe.utils.user import get_system_managers
from bs4 import BeautifulSoup
import frappe.permissions
import frappe.share
import re
import json


@frappe.whitelist()
def check_role(doc,method):
	
	glodef = frappe.get_doc("Global Defaults")
	if glodef.role_buying_price_list:
		check_pembelian = frappe.db.sql(""" SELECT NAME FROM `tabHas Role` WHERE parent = "{}" AND role = "{}" """.format(doc.name, glodef.role_buying_price_list))
		if len(check_pembelian) > 0:
			# buat user permission user ini
			check_role = frappe.db.sql(""" SELECT * FROM `tabUser Permission` WHERE user = "{}" AND allow = "Tipe Transaksi" AND for_value = "Buying" """.format(doc.name))
			if len(check_role) < 1:
				up_check_pembelian = frappe.new_doc("User Permission")
				up_check_pembelian.user = doc.name
				up_check_pembelian.allow = "Tipe Transaksi"
				up_check_pembelian.for_value = "Buying"
				up_check_pembelian.apply_to_all_doctypes = 0
				up_check_pembelian.applicable_for = "Item Price"
				up_check_pembelian.save()
		else:
			frappe.db.sql(""" DELETE FROM `tabUser Permission` WHERE user = "{}" and allow = "Tipe Transaksi" and for_value = "Buying" """.format(doc.name))

	if glodef.role_selling_price_list:
		check_penjualan = frappe.db.sql(""" SELECT NAME FROM `tabHas Role` WHERE parent = "{}" AND role = "{}" """.format(doc.name, glodef.role_selling_price_list))
		if len(check_penjualan) > 0:
			# buat user permission user ini
			check_role = frappe.db.sql(""" SELECT * FROM `tabUser Permission` WHERE user = "{}" AND allow = "Tipe Transaksi" AND for_value = "Selling" """.format(doc.name))
			if len(check_role) < 1:
				up_check_penjualan = frappe.new_doc("User Permission")
				up_check_penjualan.user = doc.name
				up_check_penjualan.allow = "Tipe Transaksi"
				up_check_penjualan.for_value = "Selling"
				up_check_penjualan.apply_to_all_doctypes = 0
				up_check_penjualan.applicable_for = "Item Price"
				up_check_penjualan.save()
		else:
			frappe.db.sql(""" DELETE FROM `tabUser Permission` WHERE user = "{}" and allow = "Tipe Transaksi" and for_value = "Selling" """.format(doc.name))
