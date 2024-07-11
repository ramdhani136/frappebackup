# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
import re, json
from frappe.realtime import publish_progress

class APICreation(Document):
	def validate(self):
		self.generate_key()

	def generate_key(self):
		if len(self.actions) > 0:
			for action in self.actions:
				action.key = action.document_type.lower().replace(" ", "_")

				# cek per trigger
				self.validate_needed_value(action=action)
		else:
			pass

	def validate_needed_value(self, action):
		if action.trigger_on == "New":
			action.field_name_mapping = None
		elif action.trigger_on == "Save":
			pass
		elif action.trigger_on == "Submit":
			action.field_mapping = None
		elif action.trigger_on == "Cancel":
			action.field_mapping = None
		elif action.trigger_on == "Delete":
			action.field_mapping = None
		else:
			action.field_name_mapping = None
			action.field_mapping = None

def run_after_insert(doc, method):
	api_creations = get_api_creation(doc=doc, method="New")
	if len(api_creations) == 0:
		return

	result = processor(doc=doc, api_creations=api_creations)
	
def run_validate(doc, method):
	api_creations = get_api_creation(doc=doc, method="Save")
	if len(api_creations) == 0:
		return

	result = processor(doc=doc, api_creations=api_creations)
	
def run_on_submit(doc, method):
	api_creations = get_api_creation(doc=doc, method="Submit")
	if len(api_creations) == 0:
		return

	result = processor(doc=doc, api_creations=api_creations)
	
def run_on_cancel(doc, method):
	api_creations = get_api_creation(doc=doc, method="Cancel")
	if len(api_creations) == 0:
		return

	result = processor(doc=doc, api_creations=api_creations)
	
def run_on_trash(doc, method):
	api_creations = get_api_creation(doc=doc, method="Delete")
	if len(api_creations) == 0:
		return

	result = processor(doc=doc, api_creations=api_creations)
	
def get_api_creation(doc, method):
	return frappe.get_all("API Creation", fields="name, document_type", filters=[['document_type', '=', doc.doctype], ['enabled', '=', 1], ['trigger_on', '=', method]])

# ===================================== ### =====================================

def processor(doc, api_creations):
	result = dict()
	doc = doc.as_dict(convert_dates_to_str=True)

	result.update({
		"doc" : doc
		})
	for api_creation in api_creations:
		apiCreation = frappe.get_doc("API Creation", api_creation['name'])
		if len(apiCreation.actions) > 0:
			index_progress_action = 1
			
			# mengubah dokumen sesuai dengan child action
			for action in apiCreation.actions:
				percent_progress = (index_progress_action/len(apiCreation.actions)) * 100
				publish_progress(percent=percent_progress, title=_("Updating {doctype}".format(doctype=action.document_type)), doctype="API Creation", docname=api_creation['name'], description=_("Please wait..."))
				index_progress_action += 1
				
				actionDoc = None
				action = action.as_dict(convert_dates_to_str=True)
				if action['is_enqueue'] == 1:
					# enqueue:
					# jika enqueue, maka variable tidak bisa dipakai untuk proses yang lainnya
					frappe.enqueue("api_integration.api_integration.doctype.api_creation.api_creation.sequential_process", doc=doc, action=action, result=result)
				else:
					# not enqueue : nanti dibuat function ke bagian enqueue
					actionDoc = sequential_process(doc=doc, action=action, result=result)
					
				if actionDoc:
					if type(actionDoc).__name__ == "list":
						value = []
						for ad in actionDoc:
							value.append(ad.as_dict(convert_dates_to_str=True))

						result.update({
							"{key}".format(key=action['key']) : value
							})
					else:
						# ini langsung doctypenya, jadi class __name__ == nama doctype tanpa spasi
						result.update({
							action['key'] : actionDoc.as_dict(convert_dates_to_str=True)
							})
				else:
					# tidak melakukan apa apa karena tidak ada dict
					pass
		else:
			# tidak melakukan apa-apa karena child action tidak ada
			pass
		# apiCreation.response = str(json.dumps(result, indent = 4))
		# apiCreation.save()

	return result

def sequential_process(doc, action, result):
	try:
		actionDoc = None
		if action['trigger_on'] == "Save":
			# membuat class doc, lalu save
			actionDoc = make_doc(doc=doc, action=action, data=result)
			if type(actionDoc).__name__ == "list":
				for ad in actionDoc:
					ad.save()
			else:
				actionDoc.save()

		elif action['trigger_on'] == "New":
			# membuat class doc, lalu insert
			actionDoc = make_doc(doc=doc, action=action, data=result)
			if type(actionDoc).__name__ == "list":
				for ad in actionDoc:
					ad.insert()
			else:
				actionDoc.insert()

		elif action['trigger_on'] == "Submit":
			# membuat class doc, lalu submit
			actionDoc = make_doc(doc=doc, action=action, data=result)
			if type(actionDoc).__name__ == "list":
				for ad in actionDoc:
					ad.submit()
			else:
				actionDoc.submit()

		elif action['trigger_on'] == "Cancel":
			# membuat class doc, lalu cancel
			actionDoc = make_doc(doc=doc, action=action, data=result)
			if type(actionDoc).__name__ == "list":
				for ad in actionDoc:
					ad.cancel()
			else:
				actionDoc.cancel()

		elif action['trigger_on'] == "Delete":
			# membuat class doc, lalu delete
			actionDoc = make_doc(doc=doc, action=action, data=result)
			if type(actionDoc).__name__ == "list":
				for ad in actionDoc:
					ad.delete()
			else:
				actionDoc.delete()
		else:
			# another trigger
			pass
		return actionDoc
	except Exception as e:
		import traceback
		err_message = "Traceback: {traceback}\nNotes: {notes}\nData: {data}".format(traceback=traceback.format_exc(), notes=e, data=doc)
		err_title = "Error API Creation: {exception}".format(exception = e)
		frappe.log_error(err_message, err_title)
		return

def make_doc(doc, action, data):
	def make(action, resultDetail):
		# make doc
		if action['trigger_on'] == "Save" or action['trigger_on'] == "Submit" or action['trigger_on'] == "Cancel" or action['trigger_on'] == "Delete":
			actionDoc = frappe.get_doc(resultDetail['doctype'], resultDetail['name'])
			actionDoc.update(resultDetail)
		else:
			actionDoc = frappe.get_doc(resultDetail)
		return actionDoc
	
	"""
	action as dict()
	"""

	# buat dict()
	resultDetail = {
		"doctype"	: action['document_type']
	}

	# get name
	if action['trigger_on'] == "Save" or action['trigger_on'] == "Submit" or action['trigger_on'] == "Cancel" or action['trigger_on'] == "Delete":
		if action['field_name_mapping'] != None and action['field_name_mapping'] != "":
			# dict untuk field name mapping
			mapping_name = json.loads(action['field_name_mapping'])
			resultDetail = compile_dict(action=action, mapping=mapping_name, resultDetail=resultDetail, data=data, is_fieldname=True)
		else:
			# ketika tidak ada field "name", maka akan di errorin
			frappe.throw(_("""Mapping for field name not found on <a href="/desk#Form/API Creation/{api_creation_name}">API Creation: {api_creation_name}</a>""".format(api_creation_name=action['parent'])))
	else:
		pass

	# dict untuk field mapping
	if type(resultDetail).__name__ == "list":
		actionDoc = []
		if len(resultDetail) > 0:
			for rd in resultDetail:
				rd = mapping_dict(action=action, resultDetail=rd, data=data)
				actionDoc.append(make(action=action, resultDetail=rd))
		else:
			pass
	elif type(resultDetail).__name__ == "dict":
		resultDetail = mapping_dict(action=action, resultDetail=resultDetail, data=data)
		actionDoc = make(action=action, resultDetail=resultDetail)
	return actionDoc

def mapping_dict(action, resultDetail, data):
	if action['field_mapping'] != None and action['field_mapping'] != "":
		mapping_fields = json.loads(action['field_mapping'])
		resultDetail = compile_dict(action=action, mapping=mapping_fields, resultDetail=resultDetail, data=data, is_fieldname=False)
	return resultDetail

def compile_dict(action, mapping, resultDetail, data, is_fieldname):
	if is_fieldname == True:
		# set filters
		filters = []
		for key, value in mapping.items():
			new_value = get_value(value=value, data=data, action=action)
			filters.append([key, '=', new_value])
		
		# get name of document
		reference_document = frappe.get_all(action['document_type'], fields="name", filters=filters)
		if len(reference_document) > 0:
			resultDetail = []
			for ref in reference_document:
				resultDetail.append({
					"doctype"	: action['document_type'],
					"name"		: ref['name']
					})
		else:
			pass
	else:
		for key, value in mapping.items():
			new_value = get_value(value=value, data=data, action=action)
			resultDetail[key] = new_value
	return resultDetail

def get_value(value, data, action):
	if isinstance(value, dict):
		new_value = []

		child_doctype = None
		index = 0
		for child_key, child_value in value.items():
			# cek nama child doctypenya
			if child_doctype == None and child_key == "_key":
				child_doctype = child_value
			else:
				pass

			if index == 0 and child_doctype == None:
				frappe.throw(_("""Key of child doctype not found on <a href="/desk#Form/API Creation/{api_creation_name}">API Creation: {api_creation_name}</a>""".format(api_creation_name=action['parent'])))
			
			if index != 0 and child_doctype != None:
				cd_index = 0
				for cd in eval("""{value}""".format(value=child_doctype)):
					indexing_child_value = child_value.replace("[i]", "[{}]".format(cd_index))
					if index == 1:
						# append new valunya
						new_value.append({
							child_key : eval("""{value}""".format(value=indexing_child_value))
							})
					elif index > 1:
						# update value di childnya
						new_value[cd_index].update({
							child_key : eval("""{value}""".format(value=indexing_child_value))
							})
					else:
						pass
					cd_index += 1
			index += 1
	else:
		password_value = get_datatype_password(data=data, value=value)
		if password_value:
			new_value = password_value
		else:
			new_value = eval("""{value}""".format(value=value))
	return new_value

def get_datatype_password(data, value):
	"""
	untuk keperluan mencari yang bertipe password

	kemungkinan isi dari value:
	1. data['doc']['password'] >> try
	2. str('Customer') >> except
	3. 0
	"""
	try:
		string = value
		find_index = string.find("][")
		# contoh dari doc_variable = "data['doc']"
		doc_variable = string.split('][')[0] + (string[find_index] if find_index > 0 else "")
		# contoh dari field = "password"
		field = string[(find_index):].split("'")[1]

		# mencari tipe dari field tsb
		doc_data = eval("""{value}""".format(value=doc_variable))
		field_datas = frappe.get_all("DocField", fields=["name", "fieldtype"], filters=[['parent', '=', doc_data['doctype']], ['fieldname', '=', field]])
		if len(field_datas) > 0:
			# jika password maka langsung diberikan value password
			if field_datas[0]['fieldtype'] == "Password":
				from frappe.utils.password import get_decrypted_password
				return get_decrypted_password(doctype=doc_data['doctype'], name=doc_data['name'], fieldname=field, raise_exception=True)
			else:
				return
		else:
			# jika tidak ditemukan maka return 
			return
	except:
		return