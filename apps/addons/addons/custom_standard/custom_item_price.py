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
def pasang_item_transaksi(doc,method):
	if doc.buying == 1:
		doc.tipe_transaksi = "Buying"
	elif doc.selling == 1:
		doc.tipe_transaksi = "Selling"