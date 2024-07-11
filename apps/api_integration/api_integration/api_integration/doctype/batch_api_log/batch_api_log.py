# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests
from frappe import _

class BatchAPILog(Document):
	def re_run_apis(self):
		self.session = requests.session()
		self.url = frappe.get_single("Batch API Tools").my_server

		try:
			from frappe.utils import get_request_session
			import json, ast

			api_logs = frappe.get_all("API Log", fields="*", filters=[['batch_api_log', '=', self.name]])
			if len(api_logs) > 0:
				idx = 0
				for log in api_logs:
					idx += 0
					frappe.publish_progress(percent=idx/len(api_logs), title=_("Sending APIs"), doctype=self.doctype, docname=self.name, description=log['name'])
					
					try:
						headers, body = {}, {}
						
						if log.get('headers', None) is not None and log.get('headers', None) != "":
							headers = ast.literal_eval(str(header_to_dict(lib=log, key='headers')))
						else:
							pass

						if log.get('data', None) is not None and log.get('data', None) != "":
							body = ast.literal_eval(str(log['data']))
						else:
							pass

						# frappe.log_error("{} || {} || {}".format(self.url, headers, body), _("PARAM"))
						res = self.session.post(self.url + log['path'] + "/", params=body, verify=True, headers=headers)
					except:
						frappe.log_error(frappe.get_traceback(), _("ERROR: Run APIs"))
			else:
				return
		except:
			frappe.log_error(frappe.get_traceback(), _("ERROR: Re Run APIs"))

def header_to_dict(lib, key):
	var = dict()
	log_headers = lib.get(key, None)
	if log_headers is not None:
		log_headers = log_headers.split("\n")
		for h in log_headers:
			header = h.split(":", 1)
			if len(header) > 1:
				if header[0] in ["Content-Type", "Authorization"]:
					var.update({
						header[0] : header[1][1:-1]
						})
				else:
					pass
			else:
				pass
	else:
		pass
	return var