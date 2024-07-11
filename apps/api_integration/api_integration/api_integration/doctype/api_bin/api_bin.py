# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class APIBin(Document):
	def validate(self):
		self.update_last_request()

	def update_last_request(self):
		self.last_request_on = frappe.utils.now()

def make_api_bin(user, headers, url, data, status_code):
	def new_bin(user, token, url, data):
		return frappe.get_doc({
			"doctype"	: "API Bin",
			"user"		: str(user),
			"token"		: str(token),
			"url"		: str(url),
			"data"		: str(data),
			"success"	: 0,
			"failed"	: 0
			})

	# get token from authorization
	headers = headers.split("\n")
	token = None
	for h in headers:
		key = h.split(":")[0]
		dataKey = h.split(":", 1)[1].lstrip(" ")
		if key == "Authorization":
			token = dataKey
			break
		else:
			pass

	# checkin uniqueness
	dataNull = False
	filters = [['user', '=', user], ['url', '=', url]]
	if data == None or data == "":
		filters.append(['data', '=', data])
		dataNull = True
	else:
		pass
	api_bins = frappe.get_all("API Bin", fields="name, data", filters=filters)
	
	# make bin
	if len(api_bins) > 0:
		if dataNull:
			api_bin = frappe.get_doc("API Bin", api_bins[0]['name'])
		else:
			# check per keyData because sequence of random variables
			import ast
			data = ast.literal_eval(data)
			for b in api_bins:
				# try except karena ada data yang null atau ''
				# jika tidak ada data, maka diabaikan, karena api menggunakan data
				try:
					b['data'] = ast.literal_eval(b['data'])
					
					countTotalDataKeyValue = 0
					countSameKeyValue = 0
					for keyData, valueData in data.items():
						countTotalDataKeyValue += 1
						for keyBin, valueBin in b['data'].items():
							if keyData == keyBin and valueData == valueBin:
								countSameKeyValue +=1
								break
							else:
								pass

					if countTotalDataKeyValue == countSameKeyValue:
						api_bin = frappe.get_doc("API Bin", b['name'])
						break
					else:
						api_bin = new_bin(user=user, token=token, url=url, data=data)
				except:
					pass
	else:
		api_bin = new_bin(user=user, token=token, url=url, data=data)

	# update count bin
	if status_code == 200:
		count = api_bin.success + 1
		api_bin.update({
			"success"	: count
			})
	else:
		count = api_bin.failed + 1
		api_bin.update({
			"failed"	: count
			})

	# save
	api_bin.save(ignore_permissions=True)