# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "addons"
app_title = "addons"
app_publisher = "PT DAS"
app_description = "addons ekatunggal"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "PT DAS"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/addons/css/addons.css"
# app_include_js = "/assets/addons/js/addons.js"

# include js, css files in header of web template
# web_include_css = "/assets/addons/css/addons.css"
# web_include_js = "/assets/addons/js/addons.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# fixtures = [
#     {"dt": "Custom Field"},
#     {"dt": "Custom Script"},
#     {"dt": "Print Format"},
#     {"dt": "Workflow"}
# ]

doctype_js = {
	"Quotation" : "public/js/quotation.js",
	"Sales Order" : "public/js/custom_sales_order.js",
	"Purchase Order" : "public/js/custom_purchase_order.js",
	"Delivery Note":"public/js/custom_delivery_note.js",
	"Sales Invoice":"public/js/sales_invoice.js",
	"Delivery Trip":"public/js/delivery_trip.js",
	"Material Request":"public/js/custom_material_request.js",
	"Stock Entry":"public/js/custom_stock_entry.js",
	"Item":"public/js/custom_item.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "addons.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "addons.install.before_install"
# after_install = "addons.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "addons.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
	"Stock Entry":{
		"validate" : "addons.custom_standard.custom_ste.check_expense",
		"before_submit": "addons.custom_so.set_ste_dll"
	},
	"Request Retur":{
		"before_submit": "addons.custom_so.set_ste_dll"
	},
	"Sales Order":{
		"autoname" : "addons.custom_so.autoname_so",
		"onload" : "addons.custom_so.net_stock_available",
		"on_submit" : "addons.custom_so.set_bottom_price",
		"before_submit": ["addons.custom_standard.custom_sales_invoice.check_max_min", "addons.custom_so.cek_qty_so_dengan_qty_qtn"],
		"on_update": "addons.custom_so.set_sales_dll",
		"on_update_after_submit": "addons.custom_so.set_sales_dll",
		"validate": [
			'addons.custom_method.validate_after_amend', 
			"addons.custom_standard.custom_sales_invoice.check_max_min", 
			# "addons.custom_standard.custom_sales_invoice.check_hpp"
		]
	},
	"Purchase Order":{
		"autoname" : "addons.custom_standard.custom_po.autoname_po",
		"on_update": "addons.custom_so.set_purchase_dll",
		"on_update_after_submit": "addons.custom_so.set_purchase_dll"
		# "onload": "addons.custom_standard.custom_po.check_price_list",
	},
	"Journal Entry":{
		"on_update": "addons.custom_so.set_journal_dll",
		"on_update_after_submit": "addons.custom_so.set_journal_dll"
	},
	"Payment Entry":{
		"on_update": "addons.custom_so.set_payment_dll",
		"on_update_after_submit": "addons.custom_so.set_payment_dll"
	},
	"Delivery Note":{
		"onload": "addons.custom_standard.custom_dn.check_workflow_customer_limit",
		"validate": ["addons.custom_standard.custom_dn.get_confirmation_doc","addons.custom_standard.custom_dn.custom_method_validate","addons.custom_standard.custom_sales_invoice.check_max_min","addons.custom_standard.custom_confirmation_document.cek_bk"],
		"before_submit" : ["addons.custom_standard.custom_sales_invoice.check_max_min","addons.custom_standard.custom_dn.custom_method_submit","addons.custom_standard.custom_check_qty_sinv_dn.overwrite_status_updater","addons.custom_standard.custom_confirmation_document.cek_bk"],
		"before_insert": ["addons.custom_standard.custom_dn.custom_method_validate","addons.custom_standard.custom_confirmation_document.cek_bk","addons.custom_standard.custom_sales_invoice.check_max_min","addons.custom_so.custom_on_insert"]
	},


	"Sales Invoice":{
		"autoname" : "addons.custom_so.autoname_sinv",
		"onload":"addons.custom_so.custom_set_status",
		"validate":["addons.custom_standard.custom_sales_invoice.check_max_min","addons.custom_standard.custom_sales_invoice.check_pajak_april"],
		"before_submit" : ["addons.custom_standard.custom_check_qty_sinv_dn.overwrite_status_updater","addons.custom_standard.custom_sales_invoice.check_max_min"]
	},
	"Delivery Trip":{
		"on_submit" : "addons.custom_standard.custom_delivery_trip.submit_delivery_notes"
	},
	"Purchase Receipt":{
		"before_submit": "addons.custom_standard.custom_purchase_invoice.cek_image_item"
	},
	"Purchase Invoice":{
		"validate" : "addons.custom_standard.custom_purchase_invoice.set_dimensi_item",
		"on_update": "addons.custom_so.set_purchase_invoice_dll",
		"on_update_after_submit": "addons.custom_so.set_purchase_invoice_dll",
		"before_submit": "addons.custom_standard.custom_purchase_invoice.cek_image_item"
	},
	"Employee Advance":{
		"before_submit" : "addons.custom_standard.custom_employee_advance.check_unfinished_advance"
	},
	"User": {
		"on_update" : "addons.custom_standard.custom_user.check_role"
	},
	"Item Price": {
		"validate" : "addons.custom_standard.custom_item_price.pasang_item_transaksi"
	},
	"Price List": {
		"validate" : "addons.custom_standard.custom_item_price.pasang_item_transaksi"
	},
	"Confirmation Document": {
		"before_submit": "addons.custom_standard.custom_confirmation_document.before_submit",
		"on_update" : "addons.custom_standard.custom_confirmation_document.validate",
		"on_trash" : "addons.custom_standard.custom_confirmation_document.on_trash"
	},
	"Quotation": {
		"before_insert" : "addons.custom_standard.custom_quotation.bersih_bersih_ordered_qty"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"addons.tasks.all"
# 	],
# 	"daily": [
# 		"addons.tasks.daily"
# 	],
# 	"hourly": [
# 		"addons.tasks.hourly"
# 	],
# 	"weekly": [
# 		"addons.tasks.weekly"
# 	]
# 	"monthly": [
# 		"addons.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "addons.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.stock.get_item_details.get_item_details": "addons.custom_standard.custom_get_item_details.get_item_details",
	"erpnext.stock.get_item_details.get_bin_details_and_serial_nos": "addons.custom_standard.custom_get_item_details.get_bin_details_and_serial_nos"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "addons.task.get_dashboard_data"
# }

