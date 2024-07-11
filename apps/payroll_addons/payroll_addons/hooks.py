# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "payroll_addons"
app_title = "Payroll Addons"
app_publisher = "DAS"
app_description = "Addons untuk Payroll Entry ERPnext v12"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
# fixtures = [
#    {"dt": "Custom Field", "filters": [
#         [
#             "dt", "in", [
#                 "Salary Slip",
#                 "Payroll Employee Detail",
#                 "Attendance"
#             ]
#         ]
#     ]},
# ]

doctype_js = {
	"Payroll Entry":"public/js/custom_payroll_entry.js"
}
# include js, css files in header of desk.html
# app_include_css = "/assets/payroll_addons/css/payroll_addons.css"
# app_include_js = "/assets/payroll_addons/js/payroll_addons.js"

# include js, css files in header of web template
# web_include_css = "/assets/payroll_addons/css/payroll_addons.css"
# web_include_js = "/assets/payroll_addons/js/payroll_addons.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
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
# get_website_user_home_page = "payroll_addons.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "payroll_addons.install.before_install"
# after_install = "payroll_addons.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "payroll_addons.notifications.get_notification_config"

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
	"Payroll Entry":{
		"validate" : "payroll_addons.custom_standard.custom_payroll_entry.override_create_slip"
	},
	"Loan":{
		"validate": "payroll_addons.custom_standard.custom_loan.overwrite_validate"
	},
	"Salary Slip":{
		"before_submit": "payroll_addons.custom_standard.custom_salary_slip.check_keterangan"
	},
	"Delivery Note":{
		"before_submit":"overdue_app.custom_check_invoice.check_overdue_invoice",
	},
	"Sales Invoice":{
		"before_submit":"overdue_app.custom_check_invoice.check_overdue_invoice",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"payroll_addons.tasks.all"
# 	],
# 	"daily": [
# 		"payroll_addons.tasks.daily"
# 	],
# 	"hourly": [
# 		"payroll_addons.tasks.hourly"
# 	],
# 	"weekly": [
# 		"payroll_addons.tasks.weekly"
# 	]
# 	"monthly": [
# 		"payroll_addons.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "payroll_addons.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "payroll_addons.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "payroll_addons.task.get_dashboard_data"
# }

