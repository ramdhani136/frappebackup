# Copyright (c) 2013, PT DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns= [
		"Item Group:Link/Item Group:120",
		"Min Qty:Float:100",
		"Item Code:Link/Item:120",
		"Item Name:Data:200",
		"Qty in All Warehouse:Float:120",
		"Stock UOM:Link/UOM:80"
	]

	data = frappe.db.sql(""" SELECT 
		tig.name,
		tig.minimum_stock,
		ti.name,
		ti.item_name,
		SUM(tb.actual_qty),
		ti.stock_uom

		FROM `tabItem Group` tig
		JOIN `tabItem` ti ON ti.item_group = tig.name
		JOIN `tabBin` tb ON tb.item_code = ti.name

		WHERE tig.is_group = 0
		GROUP BY ti.name
		""")
	return columns, data
