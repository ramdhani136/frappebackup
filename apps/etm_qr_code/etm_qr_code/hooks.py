from . import __version__ as app_version

app_name = "etm_qr_code"
app_title = "ETM QR Code"
app_publisher = "DAS DEV"
app_description = "An ETM apps for generate QR Code"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "das@das.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/etm_qr_code/css/etm_qr_code.css"
# app_include_js = "/assets/etm_qr_code/js/etm_qr_code.js"

# include js, css files in header of web template
# web_include_css = "/assets/etm_qr_code/css/etm_qr_code.css"
# web_include_js = "/assets/etm_qr_code/js/etm_qr_code.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "etm_qr_code/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "etm_qr_code.install.before_install"
# after_install = "etm_qr_code.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "etm_qr_code.uninstall.before_uninstall"
# after_uninstall = "etm_qr_code.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "etm_qr_code.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"etm_qr_code.tasks.all"
# 	],
# 	"daily": [
# 		"etm_qr_code.tasks.daily"
# 	],
# 	"hourly": [
# 		"etm_qr_code.tasks.hourly"
# 	],
# 	"weekly": [
# 		"etm_qr_code.tasks.weekly"
# 	]
# 	"monthly": [
# 		"etm_qr_code.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "etm_qr_code.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "etm_qr_code.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "etm_qr_code.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"etm_qr_code.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
