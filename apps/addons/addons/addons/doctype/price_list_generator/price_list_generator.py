# -*- coding: utf-8 -*-
# Copyright (c) 2021, PT DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PriceListGenerator(Document):
	def validate(self):
		if self.valid_from_date and self.valid_to_date:
			if self.valid_from_date > self.valid_to_date:
				frappe.throw("Date not valid, please check again.")

		if self.filter_by == "Item Code":
			if not self.item_code_table:
				frappe.throw("Please Set your Item Code.")
			else:
				self.item_code = self.item_code_table[0].item_code
				self.item_name = self.item_code_table[0].item_name

		else:
			if not self.parent_item_group:
				frappe.throw("Please Set your Item Group.")
		if self.tipe_price_list == "Selling":
			supplier = ""
		elif self.tipe_price_list == "Buying":
			customer = ""
		self.update_min_price_items()


	def get_min_price(self,item_code):
		min_price = 0
		if self.tipe_price_list == "Selling":
			sell_settings = frappe.get_doc('Selling Settings');
			if sell_settings.minimum_price_list:
				get_min_price = frappe.db.sql("""
					SELECT price_list_rate, valid_from, valid_upto FROM `tabItem Price` 
					WHERE item_code = "{}" 
					AND price_list = "{}"
					AND (valid_from IS NULL OR `valid_from` <= DATE(NOW()))
					AND (valid_upto IS NULL OR valid_upto >= DATE(NOW())) 
					LIMIT 1
				""".format(item_code, sell_settings.minimum_price_list))
				if len(get_min_price) > 0:
					min_price = get_min_price[0][0]
		return min_price

	def on_submit(self):
		if self.filter_by == "Item Code":
			if self.item_code_table:
				for tabel_item in self.item_code_table:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` 
							WHERE item_code = "{}"
							and warehouse = "{}" 
							and valuation_rate > 0
							ORDER BY DATE(posting_date) DESC
							""".format(tabel_item.item_code,sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(tabel_item.item_code,float(check_hpp[0][0])))
				
				for tabel_item in self.item_code_table:
					self.generate_price_list(tabel_item.item_code)
				
		elif self.filter_by == "Item Group":

			if self.parent_item_group and not self.item_group:
				# berarti semua item group punya parent itu
				get_item_group = frappe.db.sql(""" SELECT lft, rgt FROM `tabItem Group` 
					WHERE name = "{}" """.format(self.parent_item_group))

				lft = 0
				rgt = 0
				if len(get_item_group) > 0:
					lft = int(get_item_group[0][0])
					rgt = int(get_item_group[0][1])

				get_all_item = frappe.db.sql(""" 
					SELECT ti.name FROM `tabItem` ti
					JOIN `tabItem Group` tig 
					on ti.item_group = tig.`name`
					WHERE ti.disabled = "0"
					AND tig.`lft` > {lft} and tig.`rgt` < {rgt} """.format(lft = lft,rgt = rgt))

				for row in get_all_item:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 """.format(str(row[0]),sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(str(row[0]),float(check_hpp[0][0])))

				for row in get_all_item:
					self.generate_price_list(str(row[0]))

			elif self.item_group:
				get_all_item = frappe.db.sql(""" SELECT name FROM `tabItem` 
					WHERE item_group = "{}" and disabled = "0" """.format(self.item_group))
				
				for row in get_all_item:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 """.format(str(row[0]),sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(str(row[0]),float(check_hpp[0][0])))

				for row in get_all_item:
					self.generate_price_list(str(row[0]))

	def generate_price_list(self, item_code):
		customer = ""
		where_customer = ""
		supplier = ""
		where_supplier = ""

		if self.tipe_price_list == "Selling":
			sell_settings = frappe.get_doc('Selling Settings');
			if sell_settings.minimum_price_list:
				get_min_price = frappe.db.sql("""
					SELECT price_list_rate, valid_from, valid_upto FROM `tabItem Price` 
					WHERE item_code = "{}" 
					AND price_list = "{}"
					AND (valid_from IS NULL OR `valid_from` <= DATE(NOW()))
					AND (valid_upto IS NULL OR valid_upto >= DATE(NOW())) 
					LIMIT 1
				""".format(item_code, sell_settings.minimum_price_list))
				if len(get_min_price) > 0:
					if float(get_min_price[0][0]) > float(self.rate):
						frappe.msgprint("Harga di bawah Minimum Price di Selling Settings menurut PL {} item {} ".format(sell_settings.minimum_price_list, item_code))
						if self.keterangan:
							self.keterangan = str(self.keterangan) + "Harga di bawah Minimum Price di Selling Settings menurut PL {} item {} <br>".format(sell_settings.minimum_price_list, item_code)
						else:
							self.keterangan = "Harga di bawah Minimum Price di Selling Settings menurut PL {} item {} <br>".format(sell_settings.minimum_price_list, item_code)
						self.db_update()

			if sell_settings.maximum_price_list:
				get_max_price = frappe.db.sql("""
					SELECT price_list_rate, valid_from, valid_upto FROM `tabItem Price` 
					WHERE item_code = "{}" 
					AND price_list = "{}"
					AND (valid_from IS NULL OR `valid_from` <= DATE(NOW()))
					AND (valid_upto IS NULL OR valid_upto >= DATE(NOW())) 
					LIMIT 1
				""".format(item_code, sell_settings.maximum_price_list))
				if len(get_max_price) > 0:
					if float(get_max_price[0][0]) < float(self.rate):
						frappe.msgprint("Harga di atas Maximum Price di Selling Settings menurut PL {} item {} ".format(sell_settings.maximum_price_list, item_code))
						if self.keterangan:
							self.keterangan = str(self.keterangan) + "Harga di atas Maximum Price di Selling Settings menurut PL {} item {} <br>".format(sell_settings.maximum_price_list, item_code)
						else:
							self.keterangan = "Harga di atas Maximum Price di Selling Settings menurut PL {} item {} <br>".format(sell_settings.maximum_price_list, item_code)
						self.db_update()

			# if float(sell_settings.minimum_price) > 0:
			# 	if self.rate < float(sell_settings.minimum_price):
			# 		frappe.msgprint("Harga di bawah Minimum Price di Selling Settings.")
			# 		self.keterangan += "Harga di bawah Minimum Price di Selling Settings."
			# if float(sell_settings.maximum_price) > 0:
			# 	if self.rate > float(sell_settings.maximum_price):
			# 		frappe.msgprint("Harga di atas Maximum Price di Selling Settings.")
			# 		self.keterangan += "Harga di atas Maximum Price di Selling Settings."

		if self.customer:
			customer = self.customer
			where_customer = """ AND customer = "{}" """.format(self.customer)
		else:
			where_customer = """ AND (customer = "" OR customer IS NULL) """

		if self.supplier:
			supplier = self.supplier
			where_supplier = """ AND supplier = "{}" """.format(self.supplier)
		else:
			where_supplier = """ AND (supplier = "" OR supplier IS NULL) """


		uom = ""
		if not self.filter_uom:
			uom = frappe.get_doc("Item", item_code).stock_uom
		else:
			uom = self.filter_uom

		check_item_price = frappe.db.sql(""" 
			SELECT name FROM `tabItem Price` 
			WHERE item_code = "{}" 
			and price_list = "{}" 
			and uom = "{}" {} {} 

			""".format(item_code,self.price_list,uom,where_customer, where_supplier))

		if len(check_item_price) > 0:
			print("tidak buat baru")
			print(str(check_item_price[0][0]))
			# wes ada
			new_item_price = frappe.get_doc("Item Price", check_item_price[0][0])
			
			new_item_price.price_list_rate = self.rate
			if self.valid_from_date:
				new_item_price.valid_from = self.valid_from_date
			else:
				new_item_price.valid_from = ""
			if self.valid_to_date:
				new_item_price.valid_upto = self.valid_to_date
			else:
				new_item_price.valid_upto = ""
			new_item_price.save()

		else:
			# belum ada
			print("buat baru")
			new_item_price = frappe.new_doc("Item Price")
			new_item_price.item_code = item_code
			new_item_price.uom = uom
			new_item_price.price_list = self.price_list
			new_item_price.price_list_rate = self.rate

			if customer:
				new_item_price.customer = customer
			if supplier:
				new_item_price.supplier = supplier
			if self.valid_from_date:
				new_item_price.valid_from = self.valid_from_date
			else:
				new_item_price.valid_from = ""
			if self.valid_to_date:
				new_item_price.valid_upto = self.valid_to_date
			else:
				new_item_price.valid_upto = ""
			new_item_price.save()

	def update_min_price_items(self):

		#creator:andy jika harga dibawah minimum price perlu approval
		if self.tipe_price_list == "Selling":
			self.minimum_price_items = []
			min_price = 0
			if self.filter_by == "Item Code":
				if self.item_code_table:
					for tabel_item in self.item_code_table:
						if self.rate < self.get_min_price(tabel_item.item_code):
							self.append("minimum_price_items",{
								"item_code" : tabel_item.item_code,
								"item_name" : tabel_item.item_name,
								"min_price" : self.get_min_price(tabel_item.item_code)
								})


			elif self.filter_by == "Item Group":
				get_all_item = []
				if self.parent_item_group and not self.item_group:
					# berarti semua item group punya parent itu
					get_item_group = frappe.db.sql(""" SELECT lft, rgt FROM `tabItem Group` 
						WHERE name = "{}" """.format(self.parent_item_group))

					lft = 0
					rgt = 0
					if len(get_item_group) > 0:
						lft = int(get_item_group[0][0])
						rgt = int(get_item_group[0][1])

					get_all_item = frappe.db.sql(""" 
						SELECT ti.name, ti.item_name, ti.item_code FROM `tabItem` ti
						JOIN `tabItem Group` tig 
						on ti.item_group = tig.`name`
						WHERE ti.disabled = "0"
						AND tig.`lft` > {lft} and tig.`rgt` < {rgt} """.format(lft = lft,rgt = rgt), as_dict = 1)

				elif self.item_group:
					get_all_item = frappe.db.sql(""" SELECT name, item_code, item_name FROM `tabItem` 
						WHERE item_group = "{}" and disabled = "0" """.format(self.item_group), as_dict = 1)
				

				for item in get_all_item:
					if self.rate < self.get_min_price(item.item_code):
						self.append("minimum_price_items",{
							"item_code" : item.item_code,
							"item_name" : item.item_name,
							"min_price" : self.get_min_price(item.item_code)
							})

	

@frappe.whitelist()
def get_history(filter_by,item_code,price_list=None):
	history_harga = 0
	query_price_list = ""
	if price_list:
		query_price_list = """ HAVING price_list = "{}" """.format(price_list)
		
	if filter_by == "Item Code":
		hasil = frappe.db.sql("""
			SELECT IFNULL(rate,0), price_list
			FROM `tabPrice List Generator` plg
			LEFT JOIN `tabPrice List Generator Item` pli ON pli.parent = plg.name
			WHERE 
			plg.item_code = "{0}" OR pli.item_code = "{0}"
			AND plg.docstatus = 1
			{1}

			ORDER BY plg.creation DESC
			LIMIT 1 """.format(item_code,query_price_list))

		if len(hasil) > 0:
			history_harga = hasil[0][0]
	else:
		hasil = frappe.db.sql("""
			SELECT IFNULL(rate,0), price_list
			FROM `tabPrice List Generator` plg
			WHERE 
			plg.parent_item_group = "{0}" OR plg.item_group = "{0}"
			AND plg.docstatus = 1
			{1}

			ORDER BY plg.creation DESC
			LIMIT 1 """.format(item_code,query_price_list))

		if len(hasil) > 0:
			history_harga = hasil[0][0]


	return history_harga


@frappe.whitelist()
def query_item_group(doctype, txt, searchfield, start, page_len, filters ):

	item_group = frappe.get_doc("Item Group",filters.get("field_parent_item_group"))

	get_item_group = frappe.db.sql(""" SELECT lft, rgt FROM `tabItem Group` WHERE name = "{}" """.format(filters.get("field_parent_item_group")))

	lft = 0
	rgt = 0
	if len(get_item_group) > 0:
		lft = int(get_item_group[0][0])
		rgt = int(get_item_group[0][1])

	return frappe.db.sql("""
			SELECT 
			tig.`name`, tig.parent_item_group
			FROM `tabItem Group` tig 

			WHERE tig.lft > {lft}
			AND tig.rgt < {rgt}
			AND tig.is_group = 0

			and ( tig.name like %(txt)s)
			ORDER BY tig.name
			limit 10

		""".format(
			lft= lft,
			rgt= rgt,
			start=start,
			page_len=page_len), {
				"txt": "%{0}%".format(txt),
				"_txt": txt.replace('%', '')
			})

@frappe.whitelist()
def generate_manual():

	list_plg = frappe.db.sql(""" 
		SELECT NAME, docstatus, workflow_state FROM `tabPrice List Generator` 
		WHERE name = "PLG-0821-00346"
		ORDER BY modified ASC """)

	for row_plg in list_plg:
		print("1")
		self = frappe.get_doc("Price List Generator", row_plg[0])

		if self.filter_by == "Item Code":
			if self.item_code_table:
				print("2")
				for tabel_item in self.item_code_table:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 """.format(tabel_item.item_code,sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(tabel_item.item_code,float(check_hpp[0][0])))
				
				for tabel_item in self.item_code_table:
					print("3")
					self.generate_price_list(tabel_item.item_code)
				
		elif self.filter_by == "Item Group":

			if self.parent_item_group and not self.item_group:
				# berarti semua item group punya parent itu
				get_item_group = frappe.db.sql(""" SELECT lft, rgt FROM `tabItem Group` 
					WHERE name = "{}" """.format(self.parent_item_group))

				lft = 0
				rgt = 0
				if len(get_item_group) > 0:
					lft = int(get_item_group[0][0])
					rgt = int(get_item_group[0][1])

				get_all_item = frappe.db.sql(""" 
					SELECT ti.name FROM `tabItem` ti
					JOIN `tabItem Group` tig 
					on ti.item_group = tig.`name`
					WHERE ti.disabled = "0"
					AND tig.`lft` > {lft} and tig.`rgt` < {rgt} """.format(lft = lft,rgt = rgt))

				for row in get_all_item:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 """.format(str(row[0]),sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(str(row[0]),float(check_hpp[0][0])))

				for row in get_all_item:
					self.generate_price_list(str(row[0]))

			elif self.item_group:
				get_all_item = frappe.db.sql(""" SELECT name FROM `tabItem` 
					WHERE item_group = "{}" and disabled = "0" """.format(self.item_group))
				
				for row in get_all_item:
					sell_settings = frappe.get_doc('Selling Settings');
					if sell_settings.warehouse_check_hpp:
						# check hpp
						check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 """.format(str(row[0]),sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 1:
							if self.rate < float(check_hpp[0][0]):
								if self.tipe_price_list == "Selling":
									frappe.throw(" Harga item {} dibawah HPP senilai {}. Mohon dicek kembali ".format(str(row[0]),float(check_hpp[0][0])))

				for row in get_all_item:
					self.generate_price_list(str(row[0]))
