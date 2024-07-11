# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class APILog(Document):
	def before_insert(self):
		self.validate_batch_api_log()

	def validate(self):
		self.make_bin()

	def validate_batch_api_log(self):
		try:
			batch_api_logs = frappe.get_all("Batch API Log", fields="name", filters=[['status', '=', 'Starting']])
			if len(batch_api_logs) > 0:
				self.batch_api_log = batch_api_logs[0]['name']
			else:
				return
		except:
			frappe.log_error(frappe.get_traceback(), _("ERROR: Validate Batch API Log"))

	def make_bin(self):
		api_settings = frappe.get_single("API Settings")
		if api_settings.enable_api_bin == 1:
			if self.status_code != None and self.status_code != "":
				from api_integration.api_integration.doctype.api_bin.api_bin import make_api_bin
				try:
					user = frappe.session.user
				except:
					user = "Administrator"

				frappe.enqueue("api_integration.api_integration.doctype.api_bin.api_bin.make_api_bin", user=user, headers=self.headers, url=self.url, data=self.data, status_code=self.status_code)
				# make_api_bin(user=user, headers=self.headers, url=self.url, data=self.data, status_code=self.status_code)
			else:
				pass
		else:
			pass

def create_api_log():
	# if frappe.request.method != 'GET':
	try:
		import json
		if frappe.request:
			url = frappe.request.url if frappe.request.url else ''
			method = frappe.request.method if frappe.request.method else ''
			headers = frappe.request.headers if frappe.request.headers else ''
			args = frappe.request.args if frappe.request.args else ''
			if args:
				args = args.to_dict(flat=False)
			data = json.loads(frappe.request.data.decode('utf-8')) if frappe.request.data else ''
			cookies = frappe.request.cookies if frappe.request.cookies else ''
			path = frappe.request.path if frappe.request.path else ''
			host = frappe.request.host if frappe.request.host else ''
			request_data = str(vars(frappe.request)) if frappe.request else ''
			request = {
				'url' : str(url),
				'method' : str(method),
				'headers' : str(headers),
				'args' : str(args),
				'data' : str(data),

				'cookies' : str(cookies),
				'path' : str(path),
				'host' : str(host),
				'request_data' : str(request_data)
			}
			request['doctype'] = 'API Log'
			new_api_log = frappe.get_doc(request)
			# For checking and masking
			if if_any_checker_blacklisted(new_api_log.request_data):
				new_api_log.request_data = str(data_encrypt(new_api_log.request_data))
			if if_any_checker_blacklisted(new_api_log.data):
				new_api_log.data = str(masking_confidential_field(new_api_log.data))
			new_api_log.save(ignore_permissions=True)
			return new_api_log.name
	except:
		pass

def update_response(name, response):
	if name != 'invalid_api_log_name' and name:
		update_api_log = frappe.get_doc("API Log", name)
		update_api_log.response = str(response)
		update_api_log.status_code = response['code']
		update_api_log.save(ignore_permissions=True)
		
def update_error(name, error):
	if name != 'invalid_api_log_name' and name:
		update_api_log = frappe.get_doc("API Log", name)
		update_api_log.error = str(error)
		update_api_log.status_code = error['code']
		update_api_log.save(ignore_permissions=True)

# ============= PASSWORD =======================
# STUB Password change value
def masking_confidential_field(some_doc_field):
	""" currently support password """
	dict_field = changing_to_dict(some_doc_field)

	key_lists = [key for key, value in dict_field.items() if checker_blacklisted(key) ]
	for item in key_lists:
		dict_field[item] = "--- confidential ---"

	return str(dict_field)
		

def changing_to_dict(item):
	try:
		import ast
		var_conf = ast.literal_eval(item)
	except:
		var_conf = item
	return var_conf
	
def if_any_checker_blacklisted(str_data):
	blacklisted = ["password","cc","pwd","card_cvv","card_name","card_exp_month","card_number"]
	for item in blacklisted:
		if item in str_data:
			return True
	return False

def checker_blacklisted(key):
	blacklisted = ["password","cc","pwd","card_cvv","card_name","card_exp_month","card_number"]
	for item in blacklisted:
		if item in key:
			return True
	return False
		

def custom_request_data(frappe_request):
	if frappe_request.get("_cached_data"):
		pass
	if frappe_request.get("data"):
		pass

# STUB Password Encryption

def data_encrypt(data):
	from cryptography.fernet import Fernet
	from frappe.utils.password import get_encryption_key

	f = Fernet(str.encode(get_encryption_key()))
	encrypted_data = f.encrypt(str.encode(str(data)))

	return encrypted_data


def data_decrypt(data):
	from cryptography.fernet import Fernet
	from frappe.utils.password import get_encryption_key

	f = Fernet(str.encode(get_encryption_key()))
	decrypted_data = f.decrypt(str.encode(data.replace("b'","").replace("'","")))
	return decrypted_data

