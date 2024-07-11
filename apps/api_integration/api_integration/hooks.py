# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "api_integration"
app_title = "Api Integration"
app_publisher = "DAS"
app_description = "API Integration for managing API within Frappe. Get, Insert, Update, Logging"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "MIT"

# Fixtures
# ------------------

# fixtures = [
# 	'API Request'
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/api_integration/css/api_integration.css"
# app_include_js = "/assets/api_integration/js/api_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/api_integration/css/api_integration.css"
# web_include_js = "/assets/api_integration/js/api_integration.js"

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
# get_website_user_home_page = "api_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "api_integration.install.before_install"
# after_install = "api_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "api_integration.notifications.get_notification_config"

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
	"*": {
		"after_insert"	: ["api_integration.api_integration.doctype.api_creation.api_creation.run_after_insert"],
		"validate"		: ["api_integration.api_integration.doctype.api_creation.api_creation.run_validate"],
		"on_submit"		: ["api_integration.api_integration.doctype.api_creation.api_creation.run_on_submit"],
		"on_cancel"		: ["api_integration.api_integration.doctype.api_creation.api_creation.run_on_cancel"],
		"on_trash"		: ["api_integration.api_integration.doctype.api_creation.api_creation.run_on_trash"]
	},
	"File": {
		"after_insert"	: ["api_integration.controllers.file_controller.generate_thumbnail_hooks"],
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"0 0 * * 1": [
			"api_integration.scheduler_events.remove_success_api"
		]
	}
}

# Testing
# -------

# before_tests = "api_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "api_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "api_integration.task.get_dashboard_data"
# }

