# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
from frappe import _
import json
import frappe

class APIRequest(Document):
	original_post = ""

	# GETTER FUNCTION
	# PARAM: 
	# post: dict object (json.loads(string))
	def get_fields(self, post):
		fields_array = []
		if self.using_fixed_field:
			fields_array = self.fields.split(",")
		
		if 'fields' in post:
			new_fields_array = []
			for item in post["fields"].split(","):
				if item in fields_array and self.using_fixed_field:
					new_fields_array.append(item)
				elif not self.using_fixed_field:
					new_fields_array.append(item)
			fields_array = new_fields_array

		if fields_array:
			if "name" not in fields_array:
				fields_array.append("name")
			return self.normalize_fields(fields_array=fields_array, contain_dot=False)
		else:
			return "*"
		# if 'fields' in post:
		# 	return self.normalize_fields(fields_array=post['fields'].split(","), contain_dot=False)
		# else:
		# 	return "*"

	def get_and_filters(self, post):
		if self.and_filters:
			and_filters = self.normalized_to_standard_variable(post, self.and_filters)
		else:
			and_filters = {}
		if 'and_filters' in post:
			and_filters.update(post['and_filters'])
			return and_filters
		else:
			return and_filters

	def get_or_filters(self, post):
		if self.or_filters:
			or_filters = self.normalized_to_standard_variable(post, self.or_filters)
		else:
			or_filters = {}

		if 'or_filters' in post:
			or_filters.update(post['or_filters'])
			return or_filters
		else:
			return or_filters

	def get_limit(self, post):
		if 'limit' in post:
			return post['limit']
		elif self.get("limit"):
			return self.get("limit")
		else:
			return 20

	def get_page(self, post):
		if 'page' in post:
			return post['page']
		elif self.get("page"):
			return self.get("page")
		else:
			return 0

	def get_order_by(self, post):
		if 'order_by' in post:
			return post['order_by']
		else:
			return self.order_by
	
	def get_sql(self, post,new_sql=""):
		return self.normalized_string_to_standard_variable(post,new_sql=new_sql if new_sql else self.sql)


	# NORMALIZATION

	def replace_variables(self,some_field=""):
		now = frappe.utils.now()
		today = frappe.utils.today()
		if some_field:
			some_field = some_field.replace('<now>', now).replace('<today>', today)
			some_field = some_field.replace('<frappe.session.user>',frappe.session.user)
		
		return some_field

	def normalized_to_standard_variable(self, post, doc_field):

		# Replace variabel
		if self.variables:
			split_variables = self.variables.split("\n")
			for item_variables in split_variables:
				if ":" in item_variables:
					default_value_item = item_variables.split(":")
					default_value = default_value_item[1] if default_value_item[1] else ""
					doc_field =  doc_field.replace("<"+default_value_item[0]+">",str(post.get(default_value_item[0],default_value)))
		doc_field = self.replace_variables(some_field=doc_field)
		doc_field = doc_field.replace("'",'"')
		return json.loads(doc_field)

	def normalized_string_to_standard_variable(self, post,new_sql=""):
		if new_sql:
			sql_template = new_sql
		else:
			sql_template = self.sql

		sql_template = sql_template.replace("<LIMIT>",str(self.get_limit(post))).replace("<PAGE>",str(self.get_page(post)*self.get_limit(post))).replace("<limit>",str(self.get_limit(post))).replace("<page>",str(self.get_page(post)*self.get_limit(post)))
		if self.variables:
			split_variables = self.variables.split("\n")
			for item_variables in split_variables:
				if ":" in item_variables:
					default_value_item = item_variables.split(":")
					default_value = default_value_item[1] if default_value_item[1] else ""
					sql_template =  sql_template.replace("<"+default_value_item[0]+">",str(post.get(default_value_item[0],default_value)))
		# Replace variabel
		# ini di comment masih nda tau
		
		sql_template = self.replace_variables(some_field= sql_template)
		print(sql_template)
		return sql_template

	def normalize_fields(self, fields_array, contain_dot=True):
		if contain_dot:
			return list(filter(lambda field: "." in field, fields_array))
		else:
			return list(filter(lambda field: "." not in field, fields_array))

	def check_sql_permission(self):
		if self.sql and self.validate_permission == True:
			permission_type = "read" if "select" in self.sql else "write"
			import re
			sql_tab_item = re.findall(r'(`tab[a-zA-Z ]+`)',self.sql)

			from frappe.permissions import has_permission
			for item in sql_tab_item:
				item = item[4:-1]
				if not has_permission(item,ptype = permission_type):
					frappe.throw("User {} can't access {} for {}".format(frappe.session.user,item,permission_type))

	def add_limit_to_sql(self,post):
		# return self.sql
		import re
		if re.search(r'(LIMIT|limit).*(OFFSET|offset)\s',self.sql):
			return self.sql
		else:
			if self.sql[:-1] == "":
				return  self.sql + " LIMIT <limit> OFFSET <page>"
			else:
				return  self.sql + " LIMIT <limit> OFFSET <page>"
		


#  ==================================== CUSTOM METHOD ===================================
# STUB CUSTOM METHOD
	def custom_method(self, post):
		#make your own custom method here with return data
		if self.identifier == "Get Item Details":
			list_to_check = ["item","customer"]
			self.check_all_key(post,list_to_check)
			if not post.get("transaction_date"):
				tr_date = frappe.utils.now()
			else:
				tr_date = post.get("transaction_date")
			response_item_details = master_get_item_details(
				warehouse = post.get("warehouse"),
				price_list = post.get("price_list"),
				customer = post.get("customer"),
				company = post.get("company"),
				transaction_date = tr_date,
				item = post.get("item"),
				uom = post.get("uom"))
			return response_item_details
		elif self.identifier == "Booking Badge Count":
			data = {}
			now = frappe.utils.now()
			data['active_booking'] = len(frappe.get_list("Booking", filters={'booking_item_type': 'Vehicle Type', 'workflow_state': 'Ongoing'}))
			data['upcoming_booking'] = len(frappe.get_list("Booking", filters={'booking_item_type': 'Vehicle Type', 'workflow_state': 'Paid'}))
			data['expired_booking'] = len(frappe.get_list("Booking", filters={'booking_item_type': 'Vehicle Type', 'workflow_state': 'Expired'}))
			data['delivery_schedule_booking'] = len(frappe.get_list("Booking", filters={'booking_item_type': 'Vehicle Type', 'workflow_state': 'Paid', 'booking_from': ('=', now), 'service_option': 'Delivery to Place'}))
			data['pickup_schedule_booking'] = len(frappe.get_list("Booking", filters={'booking_item_type': 'Vehicle Type', 'workflow_state': 'Paid', 'booking_to': ('=', now), 'service_option': 'Delivery to Place'}))
# 			SELECT
# (SELECT COUNT(*) FROM `tabBooking` WHERE booking_item_type='Vehicle Type' AND workflow_state = 'Ongoing') as active_booking,
# (SELECT COUNT(*) FROM `tabBooking` WHERE booking_item_type='Vehicle Type' AND workflow_state = 'Paid') as upcoming_booking,
# (SELECT COUNT(*) FROM `tabBooking` WHERE booking_item_type='Vehicle Type' AND workflow_state = 'Expired') as expired_booking,
# (SELECT COUNT(*) FROM `tabBooking` WHERE booking_item_type='Vehicle Type' AND workflow_state = 'Paid' AND booking_from <= NOW() AND service_option = 'Delivery to Place') as delivery_schedule_booking,
# (SELECT COUNT(*) FROM `tabBooking` WHERE booking_item_type='Vehicle Type' AND workflow_state = 'Ongoing' AND booking_to <= NOW() AND service_option = 'Delivery to Place') as pickup_schedule_booking
			return [data]
		# elif self.identifier == "Get API Secret":
		# 	token = create_or_update_secret_key(post["user"])
		# 	return token
		elif self.identifier == "Validate API Secret":
			token = validate_token(post["token"])
			if token["data"] == 1:
				return {"description" : "User Valid", "valid" : 1}
			else:
				return {"description" : "User not Valid", "valid" : 0}
		elif self.identifier == "Get API Secret":
			user = post.get("user")
			if not user:
				user = post.get("email")
			password= post.get("password")
			if not password:
				password = post.get("new_password")
			response = get_api_key_with_password(user,password)
			return response
			
					

	def check_all_key(self,post, list_to_check):
		for item in list_to_check:
			if post.get(item,"") == "":
				frappe.throw(_("Key "+item+" required!"))
				frappe.flags.error_message = (_("Key "+item+" required!"))

	def test_api(self):
		data = self.read({})
		self.response = json.dumps(data, indent=4, sort_keys=True, default=str)
		print(str(self.response))

	# def read(self, post):
	# 	if self.doc_action == 'frappe.db.sql':
	# 		data = frappe.db.sql(self.get_sql(post), as_dict=True)
	# 		return data
	# 	elif self.doc_action == 'frappe.get_list':
	# 		doctype = self.document
	# 		fields =  self.get_fields(post)
	# 		filters = self.get_and_filters(post)
	# 		or_filters = self.get_or_filters(post)
	# 		limit = self.get_limit(post) 
	# 		page = self.get_page(post)
	# 		order_by = self.get_order_by(post)


	# 		data = frappe.get_list(doctype,
	# 				fields=fields,
	# 				filters=filters,
	# 				or_filters=or_filters,
	# 				limit_page_length=limit,
	# 				limit_start=page,
	# 				order_by=order_by)


	# 		# get child data
	# 		if 'fields' in post:
	# 			self.add_child_data(post, data)

	# 		return data
	# 	elif self.doc_action == 'frappe.get_all':
	# 		doctype = self.document
	# 		fields =  self.get_fields(post)
	# 		filters = self.get_and_filters(post)
	# 		or_filters = self.get_or_filters(post)
	# 		limit = self.get_limit(post) 
	# 		page = self.get_page(post)
	# 		order_by = self.get_order_by(post)


	# 		data = frappe.get_all(doctype,
	# 				fields=fields,
	# 				filters=filters,
	# 				or_filters=or_filters,
	# 				limit_page_length=limit,
	# 				limit_start=page,
	# 				order_by=order_by)

	# 		# get child data
	# 		if 'fields' in post:
	# 			self.add_child_data(post, data)
				

	# 		return data
	# 	elif self.doc_action == 'frappe.get_doc':
	# 		doctype = self.document
	# 		filters = self.get_and_filters(post)
	# 		print(filters)
	# 		data = frappe.get_doc(doctype=doctype,filters= filters)
	# 		return data
	# 	elif self.doc_action == 'frappe.get_doc_json':
	# 		doctype = self.document
	# 		filters = self.get_and_filters(post)
	# 		print(str(filters))
	# 		data = get_list_doctype(doctype,filters)
	# 		return data
	# 	elif self.doc_action == 'frappe.get_single' :
	# 		data = frappe.get_doc(self.document,self.document)
	# 		return data
	# 	elif self.doc_action == 'method':
	# 		data = self.custom_method(post)
	# 		return data

	def add_child_data(self, post, data):
		for d in data:
			parent = d['name']
			added_data = []
			
			child_fields = self.normalize_fields(fields_array=post['fields'].split(","), contain_dot=True)
			max_iteration = len(child_fields)
			iteration = 0
			while (len(child_fields) > 0 and iteration < max_iteration):
				iteration += 1 
				child_field = child_fields[0].split('.')[0]
				child_doctype = self.find_child_doctype(self.document,child_field)
				if len(child_doctype) > 0:
					child_doctype_fields = ",".join(self.find_friend_field(child_fields,child_field)).replace(child_field+".","")
					d[child_field] = frappe.get_all(child_doctype[0].options, fields=child_doctype_fields, filters={"parent":parent}, order_by="idx ASC")
					added_data.append(child_field)
				child_fields = self.exclude_array(child_fields, added_data)
		return data

	#find another field corelate with child field
	def find_friend_field(self, fields_array, fieldname):
		return list(filter(lambda field: fieldname in field, fields_array))
	def find_other_field(self, fields_array, fieldname):
		return list(filter(lambda field: fieldname not in field, fields_array))
	def find_child_doctype(self, doctype_meta, child_field):
		return list(filter(lambda field: field.fieldtype == 'Table' and field.fieldname == child_field, frappe.get_meta(doctype_meta).fields))
	def exclude_array(self, array, exclude_array):
		new_array = []
		for exclude in exclude_array:
			new_array.extend(list(filter(lambda item: exclude not in item, array)))
		return new_array

	
	# READ ini yang antz develop
	def read(self, post):

		# Experimental
		if not self.original_post:
			self.original_post = post
		if self.doc_action == 'frappe.db.sql':
			self.check_sql_permission()
			new_sql = self.add_limit_to_sql(post)
			print(new_sql)
			data = frappe.db.sql(self.get_sql(post,new_sql=new_sql), as_dict=True)
			
		
		elif self.doc_action == 'frappe.get_list':
			doctype = self.document
			fields =  self.get_fields(post)
			filters = self.get_and_filters(post)
			or_filters = self.get_or_filters(post)
			limit = self.get_limit(post) 
			page = self.get_page(post)
			order_by = self.get_order_by(post)


			data = frappe.get_list(doctype,
					fields=fields,
					filters=filters,
					or_filters=or_filters,
					limit_page_length=limit,
					limit_start=page,
					order_by=order_by)


			# get child data
			if 'fields' in post and data:
				self.add_child_data(post, data)

		elif self.doc_action == 'frappe.get_all':
			doctype = self.document
			fields =  self.get_fields(post)
			filters = self.get_and_filters(post)
			or_filters = self.get_or_filters(post)
			limit = self.get_limit(post) 
			page = self.get_page(post)
			order_by = self.get_order_by(post)


			data = frappe.get_all(doctype,
					fields=fields,
					filters=filters,
					or_filters=or_filters,
					limit_page_length=limit,
					limit_start=page,
					order_by=order_by)

			# get child data
			if 'fields' in post and data:
				self.add_child_data(post, data)
				
		elif self.doc_action == 'frappe.get_doc':
			doctype = self.document
			filters = self.get_and_filters(post)
			fields = self.get_fields(post)
			data = [get_list_doctype(doctype,filters,fields=fields)]
		elif self.doc_action == 'frappe.get_single' :
			doctype = self.document
			fields = self.get_fields(post)
			data = [get_list_doctype(doctype,doctype,fields=fields)]

		elif self.doc_action == 'method':
			if self.variables:
				split_variables = self.variables.split("\n")
			for item_variables in split_variables:
				if ":" in item_variables:
					default_value_item = item_variables.split(":")
					default_value = default_value_item[1] if default_value_item[1] else ""
					if not post.get(default_value_item[0]):
						post[default_value_item[0]] = default_value
			data = self.custom_method(post)
			
		
		if self.get("api_request_chain"):
			for item_chain in self.api_request_chain:
				doc = frappe.get_doc("API Request",item_chain.api_request)		
				for d in data:
					if d:
						chain_post = {}
						if item_chain.chain_fields:
							chain_post["fields"] = item_chain.chain_fields
						if item_chain.key_pair != "" and item_chain.key_pair:
							list_item_pair = item_chain.key_pair
							list_item_pair = list_item_pair.split("\n")
							for item_pair_per_row in list_item_pair:
								item_pair_checker = item_pair_per_row.split(":")
								if (doc.doc_action == "frappe.get_all" or doc.doc_action == "frappe.get_list"):
									if not chain_post.get("and_filters"):
										chain_post["and_filters"] = {}
									if d.get(item_pair_checker[0]):
										value_item_source = d[item_pair_checker[0]]
									else:
										value_item_source = item_pair_checker[0]
									chain_post["and_filters"].update({item_pair_checker[1] : ["=",value_item_source]})
								else:
									chain_post.update({item_pair_checker[1] : d[item_pair_checker[0]]})
						data_chain = doc.read(chain_post)
						d[item_chain.key_replace]= (data_chain)
		if len(data) ==1:
			if not data[0]:
				data = []
		return data

#=============================== SECTION get_doc_json

def to_encode(some_bytes):
	""" Function for get_doc (encode) """
	encoding = 'utf-8'
	return some_bytes.decode(encoding)

def getdoc_simplified(doctype, name, user=None):
	""" Function for get_doc build response """
	if not name:
		name = doctype
	if not frappe.db.exists(doctype, name):
		return []
	doc = frappe.get_doc(doctype, name)
	# if not doc.has_permission("read"):
	# 	if type(frappe.flags.error_message) == dict :
	# 		frappe.flags.error_message.append({"custom_err" :  ('Insufficient Permission for {}').format(frappe.bold(doctype + ' ' + name) )
	# 	else:
	# 		frappe.flags.error_message = _('Insufficient Permission for {0}').format(frappe.bold(doctype + ' ' + name))
	# 	raise frappe.PermissionError(("read", doctype, name))
	# doc.add_seen()
	frappe.response.docs = doc

import json
from frappe.utils.response import build_response
@frappe.whitelist(allow_guest=False)
def get_list_doctype(doctype,name,fields=[]):
	frappe.response.docs = []
	getdoc_simplified(doctype,name)
	js = build_response("json")
	response = json.loads(to_encode(js.get_data()))
	frappe.response.docs = []
	# as a lookup value
	response_doc = response["docs"] if response.get("docs","") else ""
	# as a dict return value
	if type(fields) == str:
		fields = fields.split(",")


	response_return = response_doc
	if fields and response_doc and "*" not in fields:
		response_return = {}
		for item_field in fields:
			response_return[item_field] = response_doc.get(item_field,"")
		
	return response_return

# !SECTION
# =================================== SECTION Function/Helper

# STUB Api Secret Key Frappe
def create_or_update_secret_key(user):
	""" args: user"""
	check_exist = frappe.db.exists("User", user)
	if check_exist:
		user_doc = frappe.get_doc("User",user)
		if user_doc.api_key:
			api_secret_string = get_password("User",user,"api_secret")
			if api_secret_string: 
				token_string = "token " + str(user_doc.api_key)+":"+str(api_secret_string)
				return {"data":1, "description" : token_string, "user" : user_doc}
		else:
			from frappe.core.doctype.user.user import generate_keys
			frappe.set_user("Administrator")
			secret = generate_keys(user)
			user_doc = frappe.get_doc("User",user)
			token_string = "token " + str(user_doc.api_key)+":"+str(secret["api_secret"]) 
			return {"data":1, "description" : token_string}
	
	frappe.throw(_("User not found. Please check your data :)"))



def validate_token(token):
	if "token " in token and ":" in token:
		token = token.replace("token ","")
		token_api_access = token.split(":")
		fga_user = frappe.get_all("User",filters=[["api_key","=",token_api_access[0]]])
		if len(fga_user) > 0:
			api_secret_string = get_password("User",fga_user[0]["name"],"api_secret")
			if token_api_access[1] == api_secret_string:
				return {"data":1, "description" : "Token Valid"}
	else:
		frappe.throw("Invalid token. Please contact administrator.")
	
	return {"data":0, "description" : "Token Invalid"}

def get_api_key_with_password(user, password):
	pass_correct = validate_password(user,password)
	user = get_user(user)
	if pass_correct == False:
		frappe.throw("Invalid email or password.")
	else:
		response = create_or_update_secret_key(user)
		if response["data"] == 1:
			if frappe.db.exists("User",user):
				doc = frappe.get_doc("User",user)
				if doc.enabled == 0:
					frappe.throw("User is disabled. Please contact Administrator")
				return {"user" : doc, "token" : response["description"]}
		else:
			frappe.throw(response["description"])
	
# STUB small function

def get_password(doctype,name,fieldname):
    '''
    Untuk mengambil password dari field Frappe yang bertipekan `password`
    '''
    from frappe.utils.password import get_decrypted_password
    d_password = get_decrypted_password(doctype, name, fieldname=fieldname, raise_exception=False)
    return d_password

def validate_password(user, password):
	from frappe.utils import cint
	from frappe.utils.password import check_password
	found_encryped_pwd = False
	try:	
		if cint(frappe.db.get_value("System Settings", "System Settings", "allow_login_using_mobile_number")):
			user = frappe.db.get_value("User", filters={"mobile_no": user}, fieldname="name") or user
		if cint(frappe.db.get_value("System Settings", "System Settings", "allow_login_using_user_name")):
			user = frappe.db.get_value("User", filters={"username": user}, fieldname="name") or user
		print(user)
		if not found_encryped_pwd:
			found_encryped_pwd = try_encrypted(user,password, "md5")
		print(found_encryped_pwd)
		if not found_encryped_pwd:
			found_encryped_pwd = try_encrypted(user,password,"sha1")
		if not found_encryped_pwd:
			# Ini kalo salah jadi kayak frappe throw
			check_password(user, password)
		return True
	except:
		return False

def get_user(user):
	from frappe.utils import cint
	user = frappe.db.get_value("User", filters={"email": user}, fieldname="name") or user
	if cint(frappe.db.get_value("System Settings", "System Settings", "allow_login_using_mobile_number")):
		user = frappe.db.get_value("User", filters={"mobile_no": user}, fieldname="name") or user
	if cint(frappe.db.get_value("System Settings", "System Settings", "allow_login_using_user_name")):
		user = frappe.db.get_value("User", filters={"username": user}, fieldname="name") or user
	return user
	

def try_encrypted(user, password, using):
	""" Supported using: md5 sha1"""
	from api_integration.helper import md5encrypt,sha1encrypt
	from frappe.utils.password import check_password
	if using == "md5":
		try:
			new_password = md5encrypt(password)
			check_password(user, new_password)
			return True
		except:
			return False
	
	elif using == "sha1":
		try:
			new_password = sha1encrypt(password)
			print(new_password)
			check_password(user, new_password)
			return True
		except:
			return False
	else:
		return False

	


# STUB Get Item Details
def master_get_item_details(warehouse, price_list,customer, company, transaction_date,item,uom=""):
	warehouse = get_default_warehouse(warehouse)
	price_list = get_default_price_list(price_list,customer)
	company = get_default_company(company)
	transaction_date = transaction_date if transaction_date else frappe.utils.now()
	#from erp...
	from erpnext.stock.get_item_details import get_item_details
	docsargs = {
		"item_code": item,
		"set_warehouse" : warehouse,
		"warehouse": warehouse,
		"customer": customer,
		"currency": "IDR",
		"price_list": price_list,
		"uom" : uom,
		"price_list_currency": "IDR",
		"plc_conversion_rate": 1,
		"conversion_rate" : 1,
		"qty" : 1,
		"company": company,
		"transaction_date": transaction_date,
		"ignore_pricing_rule": 0,
		"doctype": "Sales Invoice"
	}
	doc_item = frappe.get_doc("Item",{"item_code" : item})
	if doc_item.has_variants==1:
		list_item = frappe.db.sql("""select i.item_code from `tabItem` i 
			left join `tabItem Price` ip on ip.item_code=i.item_code and ip.price_list="{}"
			where i.variant_of="{}" and i.disabled=0
			order by ip.price_list_rate asc
			limit 0,1
			""".format(price_list,item),as_list=True)
		if len(list_item)==0:
			return {"item" : doc_item.as_dict()}
		docsargs["item_code"] = list_item[0][0]
	data = get_item_details(docsargs)
	
	return {"item_detail" : data, "item" : doc_item.as_dict()}

def get_default_company(company="", user=""):
	default_company = frappe.get_value("Global Defaults","Global Defaults","default_company")
	if company:
		return company
	else:
		fg_company = frappe.get_list("Company",fields="name")
		if len(fg_company) > 0:
			return fg_company[0]["name"]
	return default_company

def get_default_warehouse(warehouse=""):
	if warehouse:
		return warehouse
	else:
		default_warehouse = frappe.get_value("Stock Settings","Stock Settings","default_warehouse")
		return default_warehouse

def get_default_price_list(price_list="", user=""):
	default_price_list = frappe.get_value("Selling Settings","Selling Settings","selling_price_list")
	if price_list:
		return price_list
	elif user:
		customer = frappe.get_all("Customer", fields= "*", filters=[["name","=",user]])
		if len(customer) > 0:
			if customer[0]["default_price_list"]:
				return customer[0]["default_price_list"] 
	
	return default_price_list


# !SECTION
