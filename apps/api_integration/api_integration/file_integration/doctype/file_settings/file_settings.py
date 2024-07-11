# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class FileSettings(Document):
	def validate(self):
		self.validate_setting_width_height()

	# End of hooks

	def validate_setting_width_height(self):
		if self.file_max_height and self.file_max_width:
			if self.file_max_height > 0 and self.file_max_width > 0 :
				frappe.throw(_("Please set height or width only, and fill the other with 0 "))
		if self.file_max_height == 0 and self.file_max_width == 0 and self.using_file_compression == 1:
			frappe.throw(_("Please set the height or width"))
