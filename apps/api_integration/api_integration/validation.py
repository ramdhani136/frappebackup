# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

def success_format(doc):
	api_settings = frappe.get_single("API Settings")
	# MICH: (3/3/2021) tambah checkbox enable api log
	if api_settings.enable_api_log == 1:
		from api_integration.api_integration.doctype.api_log.api_log import create_api_log, update_response, update_error
		api_log_name = create_api_log()
	
	data = dict()
	data['code'] = 200
	data['data'] = doc

	# set response http status code
	# frappe.local.response.http_status_code = data['code']

	if api_settings.enable_api_log == 1:
		update_response(name = api_log_name, response = data)
	return data

def error_format(exceptions, code=500, err_text="", indicator="red"):
	import json, sys, traceback
	from frappe import _

	api_settings = frappe.get_single("API Settings")
	# MICH: (3/3/2021) tambah checkbox enable api log
	if api_settings.enable_api_log == 1:
		# create api log
		from api_integration.api_integration.doctype.api_log.api_log import create_api_log, update_response, update_error
		api_log_name = create_api_log()

	# default value
	data = dict()
	if err_text:
		data['error'] = str(err_text)
	elif exceptions:
		data['error'] = str(exceptions)
	else:
		data['error'] = ""
	data['code'] = code
	data['indicator'] = indicator

	# frappe local message
	if frappe.local.message_log:
		data['server_messages'] = [json.loads(frappe.utils.cstr(d)) for
			d in frappe.local.message_log]
		data['error'] = data['server_messages'][0]['message']

	if frappe.debug_log and frappe.conf.get("logging") or False:
		data['debug_messages'] = frappe.local.debug_log

	if frappe.flags.error_message:
		data['error'] = frappe.flags.error_message
		data['error_message'] = frappe.flags.error_message

	# trace for developer
	exc_type, exc_value, exc_tb = sys.exc_info()
	trace_list = traceback.format_exception(exc_type, exc_value, exc_tb)
	data['trace_list'] = trace_list

	try:
		last_trace_list = trace_list[-1].split(":")[0].split(".")[-1]
		http_status_code = getattr(frappe, "{}".format(last_trace_list)).http_status_code
		data['error_type'] = last_trace_list
		data['code'] = http_status_code
	except:
		pass

	# set response http status code
	# frappe.local.response.http_status_code = data['code']

	if api_settings.enable_api_log == 1:
		# update api log
		update_error(name = api_log_name, error = data)

	return data

# ==================================== Validation ====================================

def doc_permlevel_value_to_null(document):
	"""
	document as object
	"""
	import copy 
	temp_document = copy.copy(document)
	document = vars(document)
	for attr in document:
		if temp_document.meta.get_field(attr) is not None:
			if temp_document.meta.get_field(attr).permlevel != 0:
				permlevel_access = temp_document.has_permlevel_access_to(fieldname=attr)
				if permlevel_access == False:
					document[attr] = None
			
			if temp_document.meta.get_field(attr).fieldtype == 'Table':
				for child_docs in document[attr]:
					childdoc_permlevel_value_to_null(child_docs)
	return document

def childdoc_permlevel_value_to_null(document):
	import copy 
	temp_document = copy.copy(document)
	document = vars(document)
	for attr in document:
		if temp_document.meta.get_field(attr) is not None:
			if temp_document.meta.get_field(attr).permlevel != 0:
				permlevel_access = temp_document.has_permlevel_access_to(fieldname=attr)
				if permlevel_access == False:
					document[attr] = None