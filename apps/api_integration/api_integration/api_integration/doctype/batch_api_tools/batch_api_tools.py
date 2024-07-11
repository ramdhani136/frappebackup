# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class BatchAPITools(Document):
	def start_batch(self):
		batch_api_logs = frappe.get_all("Batch API Log", fields="name", filters=[['status', '=', 'Starting']])
		if len(batch_api_logs) > 0:
			frappe.throw(_("Masih ada batch API yang sedang berjalan. Klik tombol berhenti terlebih dahulu untuk memulai batch yang baru"))
		else:
			batch_api_log = frappe.get_doc({
				"doctype"		: "Batch API Log",
				"status"		: "Starting",
				"start_on"		: frappe.utils.now()
				})
			batch_api_log.save(ignore_permissions=True)

	def stop_batch(self):
		batch_api_logs = frappe.get_all("Batch API Log", fields="name", filters=[['status', '=', 'Starting']])
		if len(batch_api_logs) > 0:
			batch_api_log = frappe.get_doc("Batch API Log", batch_api_logs[0]['name'])
			batch_api_log.update({
				"status"	: "Done",
				"end_on"	: frappe.utils.now()
				})
			batch_api_log.save(ignore_permissions=True)
		else:
			frappe.throw(_("Tidak ada batch yang berjalan. Klik tombol mulai untuk memulai batch yang baru"))