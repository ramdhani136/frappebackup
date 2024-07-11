# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
# from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc

@frappe.whitelist()
def check_tanggal():
	doc = frappe.get_doc("Sales Invoice", "SJ-2022-03-00015")
	if doc.posting_date and doc.taxes:
		print(frappe.utils.date_diff(doc.posting_date, "2022-03-31"))
		if frappe.utils.date_diff(doc.posting_date, "2022-03-31") > 0:
			for row in doc.taxes:
				if row.rate == 10:
					row.rate == 11
					print("TEST")
	# print(frappe.utils.date_diff("2022-04-01", "2022-03-31"))

@frappe.whitelist()
def check_pajak_april(doc,method):
	if doc.posting_date and doc.taxes:
		print(frappe.utils.date_diff(doc.posting_date, "2022-03-31"))
		if frappe.utils.date_diff(doc.posting_date, "2022-03-31") > 0:
			for row in doc.taxes:
				if row.rate == 10:
					row.rate = 11
					doc.run_method("calculate_taxes_and_totals")
					
@frappe.whitelist()
def check_max_min(doc,method):
	sell_settings = frappe.get_doc('Selling Settings');
	if doc.doctype == "Delivery Note" or doc.doctype == "Sales Invoice" or doc.doctype == "Purchase Invoice" or doc.doctype == "Purchase Receipt":
		 if doc.is_return == 1:
		 	return

	if (doc.docstatus == 0 or doc.get("__islocal")):
		if sell_settings.warehouse_check_hpp:
			
			# check hpp
			counter = 1
			item_rate = ''
			for item in doc.items:
				bypass_hpp = 0
				if doc.doctype == "Sales Invoice" or doc.doctype == "Delivery Note":
					if "Bypass SINV" in frappe.get_roles(frappe.session.user):
						bypass_hpp = 1
					if item.so_detail:
						check_qtn = frappe.db.sql(""" SELECT prevdoc_docname FROM `tabSales Order Item` WHERE name = "{}" AND prevdoc_docname IS NOT NULL """.format(item.so_detail))
						if len(check_qtn) > 0:
							bypass_hpp = 1
						else:
							check_prec = frappe.db.sql(""" SELECT rate , `tabPurchase Receipt`.name
								FROM `tabPurchase Receipt Item` Join `tabPurchase Receipt` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
								WHERE item_code = "{}" 
								and warehouse = "{}"
								AND `tabPurchase Receipt`.docstatus = 1
								ORDER BY TIMESTAMP(posting_date,posting_time) DESC
								""".format(item.item_code,sell_settings.warehouse_check_hpp))
							if len(check_prec) > 0:
								if item.rate < float(check_prec[0][0]):
									item_rate += " Harga item {} di row {} dibawah Harga Beli Terakhir senilai {}-{}. Mohon dicek kembali ".format(item.item_code,counter,float(check_prec[0][0]),check_prec[0][1]) + '<br>'
									bypass_hpp = 0
							else:
								check_hpp = frappe.db.sql(""" SELECT valuation_rate 
									FROM `tabStock Ledger Entry` 
									WHERE item_code = "{}" 
									and warehouse = "{}"
									and valuation_rate > 0 
									AND docstatus = 1
									AND is_cancelled = 0
									ORDER BY TIMESTAMP(posting_date,posting_time) DESC
									""".format(item.item_code,sell_settings.warehouse_check_hpp))
								if len(check_hpp) > 0:
									if item.rate < float(check_hpp[0][0]):
										item_rate += " Harga item {} di row {} dibawah HPP . Mohon dicek kembali ".format(item.item_code,counter,float(check_hpp[0][0])) + '<br>'
										bypass_hpp = 0


				elif doc.doctype == "Sales Order":
					
					if item.prevdoc_docname is None:
						check_prec = frappe.db.sql(""" SELECT rate , `tabPurchase Receipt`.name
							FROM `tabPurchase Receipt Item` Join `tabPurchase Receipt` on 
							`tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
							WHERE item_code = "{}" 
							and warehouse = "{}"
							AND `tabPurchase Receipt`.docstatus = 1
							ORDER BY TIMESTAMP(posting_date,posting_time) DESC
							""".format(item.item_code,sell_settings.warehouse_check_hpp))
						if len(check_prec) > 0:

							if item.rate < float(check_prec[0][0]):
								item_rate += " Harga item {} di row {} dibawah Harga Beli Terakhir senilai {}-{}. Mohon dicek kembali ".format(item.item_code,counter,float(check_prec[0][0]),check_prec[0][1]) + '<br>'
								bypass_hpp = 0
						else:
							check_hpp = frappe.db.sql(""" SELECT valuation_rate 
								FROM `tabStock Ledger Entry` 
								WHERE item_code = "{}" 
								and warehouse = "{}"
								and valuation_rate > 0 
								AND docstatus = 1
								AND is_cancelled = 0
								ORDER BY TIMESTAMP(posting_date,posting_time) DESC
								""".format(item.item_code,sell_settings.warehouse_check_hpp))
							if len(check_hpp) > 0:
								if item.rate < float(check_hpp[0][0]):
									item_rate += " Harga item {} di row {} dibawah HPP . Mohon dicek kembali ".format(item.item_code,counter,float(check_hpp[0][0])) + '<br>'
									bypass_hpp = 0
					else:
						bypass_hpp = 1

					# else:
					# 	bypass_hpp = 0

				# # if bypass_hpp == 0:
				# if "Bypass SINV" not in frappe.get_roles(frappe.session.user) and doc.doctype != "Sales Order":
				# 	check_hpp = frappe.db.sql(""" SELECT valuation_rate 
				# 		FROM `tabStock Ledger Entry` 
				# 		WHERE item_code = "{}" 
				# 		and warehouse = "{}"
				# 		and valuation_rate > 0 
				# 		AND docstatus = 1
				# 		AND is_cancelled = 0
				# 		ORDER BY TIMESTAMP(posting_date,posting_time) DESC
				# 		""".format(item.item_code,sell_settings.warehouse_check_hpp))
				# 	if len(check_hpp) > 0:
				# 		if item.rate < float(check_hpp[0][0]):
				# 			item_rate += " Harga item {} di row {} dibawah HPP . Mohon dicek kembali ".format(item.item_code,counter,float(check_hpp[0][0])) + '<br>'
				
				if bypass_hpp == 0:
					if "Bypass SINV" not in frappe.get_roles(frappe.session.user):
						check_hpp = frappe.db.sql(""" SELECT valuation_rate 
							FROM `tabStock Ledger Entry` 
							WHERE item_code = "{}" 
							and warehouse = "{}"
							and valuation_rate > 0 
							AND docstatus = 1
							AND is_cancelled = 0
							ORDER BY TIMESTAMP(posting_date,posting_time) DESC
							""".format(item.item_code,sell_settings.warehouse_check_hpp))
						if len(check_hpp) > 0:
							if item.rate < float(check_hpp[0][0]):
								item_rate += " Harga item {} di row {} dibawah HPP . Mohon dicek kembali ".format(item.item_code,counter,float(check_hpp[0][0])) + '<br>'
					
				counter = counter + 1

			if item_rate and bypass_hpp == 0:
				frappe.throw(item_rate)

		if sell_settings.minimum_price_list:
			frappe.db.sql(""" UPDATE `tab{}` SET minimum_price = "{}" WHERE name = "{}" """.format(doc.doctype, sell_settings.minimum_price_list, doc.name))
			counter = 1
			for item in doc.items:
				if sell_settings.minimum_price_list:
					doc.minimum_price = sell_settings.minimum_price_list
					get_min_price = frappe.db.sql("""
						SELECT price_list_rate, valid_from, valid_upto FROM `tabItem Price` 
						WHERE item_code = "{}" 
						AND price_list = "{}"
						AND (valid_from IS NULL OR `valid_from` <= DATE(NOW()))
						AND (valid_upto IS NULL OR valid_upto >= DATE(NOW())) 
						LIMIT 1
					""".format(item.item_code, sell_settings.minimum_price_list))
					if len(get_min_price) > 0:
						item.minimum_price_hint = float(get_min_price[0][0])
						if float(get_min_price[0][0]) > float(item.rate):
							frappe.msgprint("Harga {} di row {} di bawah Minimum Price di Selling Settings menurut PL {}".format(item.item_code,counter, sell_settings.minimum_price_list))
					else:
						item.minimum_price_hint = 0
				counter = counter + 1

		if sell_settings.maximum_price_list:
			frappe.db.sql(""" UPDATE `tab{}` SET maximum_price = "{}" WHERE name = "{}" """.format(doc.doctype, sell_settings.maximum_price_list, doc.name))		
			counter = 1
			for item in doc.items:
				if sell_settings.maximum_price_list:
					doc.maximum_price = sell_settings.maximum_price_list
					get_max_price = frappe.db.sql("""
						SELECT price_list_rate, valid_from, valid_upto FROM `tabItem Price` 
						WHERE item_code = "{}" 
						AND price_list = "{}"
						AND (valid_from IS NULL OR `valid_from` <= DATE(NOW()))
						AND (valid_upto IS NULL OR valid_upto >= DATE(NOW())) 
						LIMIT 1
					""".format(item_code, sell_settings.maximum_price_list))
					if len(get_max_price) > 0:
						item.maximum_price_hint = float(get_max_price[0][0])
						# if float(get_max_price[0][0]) < float(self.rate):
						# 	frappe.msgprint("Harga {} di row {} di bawah Minimum Price di Selling Settings menurut PL {}".format(item.item_code,counter, sell_settings.maximum_price_list))
					else:
						item.maximum_price_hint = 0

				counter = counter + 1
	# frappe.throw("fail")

@frappe.whitelist()
def check_hpp(doc,method):
	# sell_settings = frappe.get_doc('Selling Settings');
	# if doc.docstatus == 0:
	# 	re_calculate = False
	# 	for item in doc.items:
	# 		if item.prevdoc_docname:
	# 			check_hpp = frappe.db.sql(""" SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE item_code = "{}" and warehouse = "{}" and valuation_rate > 0 ORDER BY TIMESTAMP(posting_date,posting_time) DESC """.format(item.item_code,sell_settings.warehouse_check_hpp))
	# 		if len(check_hpp) > 0:
	# 			if item.rate < float(check_hpp[0][0]):
	# 				re_calculate = True
	# 				item.rate = float(check_hpp[0][0])
	# 				frappe.msgprint(str(item.rate))

	# 	frappe.msgprint('-------')
	# 	frappe.msgprint(str(doc.items[0].rate))
	# 	frappe.msgprint(str(doc.items[1].rate))
	# 	frappe.msgprint(str(doc.items[2].rate))
	# 	frappe.msgprint(str(doc.items[3].rate))
	# 	frappe.msgprint('-------')
	# 	if re_calculate:
	# 		doc.run_method('calculate_taxes_and_totals')
	# 	frappe.msgprint(str(doc.items[0].rate))
	# 	frappe.msgprint(str(doc.items[1].rate))
	# 	frappe.msgprint(str(doc.items[2].rate))
	# 	frappe.msgprint(str(doc.items[3].rate))
	# 	frappe.msgprint(str(doc.grand_total))

	# 	frappe.throw('tes')
	return


		
