# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "overdue_app"
app_title = "Overdue App"
app_publisher = "chandra-das"
app_description = "app untuk membatasi jumlah invoice ketika ada overdue dari customer yang sama. contoh diset 1, maka customer tidak bisa lanjut submit untuk berikut - berikutnya ketika masih overdue."
app_icon = "octicon octicon-file-directory"
app_color = "red"
app_email = "nugraha.chandrasatria@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

fixtures = [
   {"dt": "Custom Field", "filters": [
        [
            "fieldname", "in", [
                "limit_customer_overdue"
            ]
        ]
    ]}
]

# include js, css files in header of desk.html
# app_include_css = "/assets/overdue_app/css/overdue_app.css"
# app_include_js = "/assets/overdue_app/js/overdue_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/overdue_app/css/overdue_app.css"
# web_include_js = "/assets/overdue_app/js/overdue_app.js"

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
# get_website_user_home_page = "overdue_app.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "overdue_app.install.before_install"
# after_install = "overdue_app.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "overdue_app.notifications.get_notification_config"

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
	"Delivery Note":{
		"onload":"overdue_app.custom_check_invoice.check_workflow_invoice_overdues",
		"validate":"overdue_app.custom_check_invoice.check_overdue_invoice_with_field",
		"before_submit":"overdue_app.custom_check_invoice.check_overdue_invoice",
	},
	"Sales Invoice":{
		"before_submit":"overdue_app.custom_check_invoice.check_overdue_invoice",
	},
	"Sales Order":{
		"before_submit":"overdue_app.custom_check_invoice.check_overdue_invoice",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"overdue_app.tasks.all"
# 	],
# 	"daily": [
# 		"overdue_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"overdue_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"overdue_app.tasks.weekly"
# 	]
# 	"monthly": [
# 		"overdue_app.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "overdue_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "overdue_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "overdue_app.task.get_dashboard_data"
# }

