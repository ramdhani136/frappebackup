# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import _
import json, sys, base64
from api_integration.helper import get_password
from api_integration.validation import error_format, success_format

def translate_error(some_error_string):
	list_translate = ["Could not find Row"]
	for item in list_translate:
		if str(some_error_string) in item:
			some_error_string = some_error_string.replace(item,(_(item)))
	return some_error_string

def validate_exist(params, json):
	for param in params:
		if param not in json:
			return param
	return None

@frappe.whitelist(allow_guest=True)
def get_image(file_url =""):
	"""
	Contoh: 
	- https://titan.bligro.com/api/method/api_integration.api_integration.request.get_image?file_url=/private/files/some_image.png
	- https://titan.bligro.com/api/method/api_integration.api_integration.request.get_image?file_url=/files/some_file.zip
	
	Jangan lupa upload file no_photo.jpg di doctype File
	"""
	import os
	from frappe.utils.file_manager import get_files_path
	import re
	import urllib.parse
	if not file_url:
		fp = get_files_path()
		file_url = "/files/no_photo.jpg"
		path = os.path.join(fp, os.path.basename("/files/no_photo.jpg"))
		with open(path, "rb") as fileobj:
			filedata = fileobj.read()
	else:

		# replace and parse file_url to make like this -> /files/test.png
		if re.search(r'(/).*(\.)[a-z|A-Z]+',file_url) and "files" not in file_url:
			file_url = "/files" + file_url
		elif re.search(r'[a-z|A-Z].*(\.)[a-z|A-Z]+',file_url) and "files" not in file_url:
			file_url = "/files/" + file_url
		elif "/" != file_url[0]:
			file_url = "/"+file_url

		print(file_url)
		file_exist = frappe.db.exists("File",{"file_url":file_url})

		if not file_exist:
			file_url= "private"+file_url
		
		fp = get_files_path()
		print(fp)
	

		# Ini menjadikan fila yang diminta public jadi private
		if "private/" in file_url:
			fp = get_files_path().replace("/public/files","/private/files/")

		# Ini cek permission
		if "private" in file_url:
			file_exist = frappe.db.exists("File",{"file_url":file_url})
			if file_exist:
				file_doc = frappe.get_doc("File", {"file_url":file_url})
				file_doc.check_permission("read")

		# Ini cek jika private tidak bisa coba pake public
		if "private" in file_url:
			path = os.path.join(fp, os.path.basename(file_url))
			try:
				with open(path, "rb") as fileobj:
					filedata = fileobj.read()
				print("private success")
			except:
				print("failed private")
				fp = get_files_path().replace("/private/files","/public/files/")
				file_url = file_url.replace("/private/files/","/public/files/")
		
		
		# Ini membaca file, kalo error baru kluarkan no_photo
		path = os.path.join(fp, os.path.basename(file_url))
		try:
			with open(path, "rb") as fileobj:
				filedata = fileobj.read()
		except:
			print("failed")
			fp = get_files_path()
			file_url = "/files/no_photo.jpg"
			path = os.path.join(fp, os.path.basename("/files/no_photo.jpg"))
			with open(path, "rb") as fileobj:
				filedata = fileobj.read()

	# frappe.local.response.filename = os.path.basename(urllib.parse.quote(file_url))
	print(os.path.basename(file_url))
	frappe.local.response.filename = os.path.basename(soft_parse(file_url))
	frappe.local.response.filecontent = filedata
	frappe.local.response.type = "download"

def soft_parse(some_value):
	some_value = some_value.replace(" ", "%20")
	return some_value

@frappe.whitelist()
def read():
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))

		# if validate_exist(["identifier"], post) is not None: ((* di comment karena kurang efektif))
		if post.get("identifier", None) == None:
			frappe.throw(_("Missing identifier"))
		request_doc = frappe.get_doc("API Request", post['identifier'])
		response = request_doc.read(post)
		if response is not None:
			return success_format(response)
		else:
			return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

# ============================ API =====================================

@frappe.whitelist(allow_guest=False)
def ping():
	try:
		if frappe.request.method == "GET":
			return success_format("pong")
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def get_session_user():
	try:
		if frappe.request.method == "GET":
			return success_format({"user" : frappe.session.user})
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def try_permission(doctype):
	try:
		if frappe.request.method == "GET":
			from frappe.permissions import has_permission
			has_permission(doctype, ptype="read", doc=None, verbose=False, user=None, raise_exception=True)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def get_doc(doctype, docname, ignore_permissions=False):
	try:
		if frappe.request.method == 'GET':
			result = frappe.get_doc(doctype, docname)
			
			if ignore_permissions:
				from api_integration.validation import doc_permlevel_value_to_null
				doc_permlevel_value_to_null(result)
				
			return success_format(result)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def get_single_doc(doctype):
	try:
		if frappe.request.method == "GET":
			response = frappe.get_single(doctype)

			return success_format(response)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def get_list(doctype,filters='',fields='*',limit=20,page=0,order_by="modified DESC"):
	try:
		if frappe.request.method == "GET":
			response = frappe.get_list(doctype,
							fields=fields,
							filters=filters,
							limit_page_length=limit,
							limit_start=page,
							order_by=order_by)

			return success_format(response)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def create_doc():
	try:
		if frappe.request.method == 'POST':
			post = json.loads(frappe.request.data.decode('utf-8'))
			doc = frappe.get_doc(post)
			doc.save()
			return success_format(doc)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def create_or_update_doc():
	"""
	{
	"doctype" : "",
	"name" : "",
	"..." : "..."
	}
	"""
	try:
		if frappe.request.method == "POST":
			do_create = 1
			post = json.loads(frappe.request.data.decode('utf-8'))
			if not post.get("doctype"):
				return error_format(exceptions=sys.exc_info(), code=500, err_text="Doctype must to be filled.", indicator="red")
			if post.get("name") and post.get("doctype"):
				doc_exist = frappe.db.exists(post["doctype"], post["name"])
				if doc_exist:
					doc = frappe.get_doc(post["doctype"], post["name"])
					doc.update(post)
					doc.save()

					result = doc
					do_create = 0
				else:
					del(post["name"])
					do_create = 1
			
			if do_create == 1:
				doc = frappe.get_doc(post)
				doc.save()
			
			result = doc
			return success_format(result)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def create_child_doc():
	# beta
	try:
		if frappe.request.method == "POST":
			post = json.loads(frappe.request.data.decode('utf-8'))
			
			count_idx = frappe.db.sql("SELECT COUNT(*) as total_record FROM `tab{}` WHERE parenttype = '{}' AND parent = '{}'".format(post['doctype'], post['parenttype'], post['parent']), as_dict=True)
			post['idx'] = count_idx[0]['total_record'] + 1

			doc = frappe.get_doc(post)
			doc.save()
			doc_parent = frappe.get_doc(post['parenttype'], post['parent'])
			doc_parent.save()
			return success_format(doc)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def create_child_doc_list():
	# beta
	try:
		if frappe.request.method == "PUT":
			post = json.loads(frappe.request.data.decode('utf-8'))
			for loop_list in post['list']:
				count_idx = frappe.db.sql("SELECT COUNT(*) as total_record FROM `tab{}` WHERE parenttype = '{}' AND parent = '{}'".format(loop_list['doctype'], loop_list['parenttype'], loop_list['parent']), as_dict=True)
				loop_list['idx'] = count_idx[0]['total_record'] + 1

				doc = frappe.get_doc(loop_list)
				doc.save()

			doc_parent = frappe.get_doc(loop_list['parenttype'], loop_list['parent'])
			doc_parent.save()

			result = frappe.get_doc("{}".format(post['list'][0]['parenttype']), "{}".format(post['list'][0]['parent']))
			return success_format(result)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def update_doc():
	"""
	{
	"doctype" : "",
	"name" : "",
	"..." : "..."
	}
	"""
	try:
		if frappe.request.method == "PUT" or frappe.request.method == "POST":
			post = json.loads(frappe.request.data.decode('utf-8'))
			doc = frappe.get_doc(post['doctype'], post['name'])

			update = False
			is_child_doc = frappe.get_value("DocType", post['doctype'], ['istable'])
			if is_child_doc:
				doctype = doc.parenttype
				name = doc.parent
			else:
				doctype = post['doctype']
				name = post['name']

			docshares = frappe.get_all("DocShare", fields="*", filters=[['user', '=', frappe.session.user], ['share_doctype', '=', doctype], ['share_name', '=', name]])
			if len(docshares) > 0:
				for d in docshares:
					if d.write == 1:
						update = True
					else:
						pass
			else:
				update = True

			if update == False:
				return error_format(exceptions=sys.exc_info(), code=500, err_text=_("Insufficient Permission for {doctype}".format(doctype=doctype)), indicator="red")

			doc.update(post)
			doc.save()
			return success_format(doc)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def delete_doc():
	"""
	{
	"doctype" : "",
	"name" : ""
	}
	"""
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		doc = frappe.delete_doc(post['doctype'], post['name'])
		return success_format({"deleted":True})
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=False)
def submit_doc():
	"""
	{
	"doctype" : "",
	"name" : ""
	}
	"""
	try:
		if frappe.request.method == 'POST':
			post = json.loads(frappe.request.data.decode('utf-8'))
			doc = frappe.get_doc(post['doctype'], post['name'])
			doc.submit()
			return success_format(doc)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

@frappe.whitelist(allow_guest=True)
def upload_file():
	from api_integration.helper import randomString
	"""
	{
	"filename" : "",
	"filedata" : "",
	"attached_to_doctype" : "",
	"attached_to_docname" : "",
	"docfield" : "",
	"is_private" : 0
	### additional field akan menambahkan data kedalam file
	additional_field = []
	}
	"""
	try:
		if frappe.request.method == "POST":
			post = json.loads(frappe.request.data.decode('utf-8'))
			
			docfield = post.get('docfield', None)
			if not post.get("filename"):
				post["filename"] = frappe.utils.now()[:10].replace("-","")+randomString(stringLength=8)+".png"
			if post.get("is_private") == 0 or post.get("is_private") == False:
				post["is_private"] = 0
			else:
				post["is_private"] = 1
			from frappe.utils.file_manager import save_file
			result = save_file(fname=post['filename'], content=post['filedata'], dt=post['attached_to_doctype'], dn=post['attached_to_docname'], folder=None, decode=True, is_private=post["is_private"], df=docfield)

			string_update_sql = ""
			if post.get("additional_field"):
				for item in post.get("additional_field"):
					item_key = item.lower().replace(" ","_")
					string_update_sql += """ {field} = "{value}",""".format(field=item_key, value= post.get(item_key,""))
				string_update_sql = string_update_sql[:-1]
				frappe.db.sql("""UPDATE `tabFile` SET {file_item_sql} WHERE name = %(result_name)s """.format(file_item_sql= string_update_sql),{
					"result_name" : result.get("name")})
					# frappe.throw(str(vars(result)))
			if docfield:
				frappe.db.sql("""
					UPDATE `tab{doctype}`
					SET {docfield} = %(value)s
					WHERE name = %(name)s
					""".format(doctype=post['attached_to_doctype'], docfield=docfield), {
					"name" : post['attached_to_docname'],
					"value" : result.file_url
					})
			
			frappe.db.commit()
			return success_format(result)
		else:
			return success_format("Invalid Method")
	except:
		return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")