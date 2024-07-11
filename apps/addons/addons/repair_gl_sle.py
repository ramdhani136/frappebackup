import frappe

@frappe.whitelist()
def operasi_stock_ledger():
	list_voucher = frappe.db.sql(""" 
		SELECT voucher_type, voucher_no,
		TIMESTAMP(posting_date,posting_time) FROM `tabStock Ledger Entry` WHERE
		WHERE docstatus = 1 AND is_cancelled = 0 AND posting_date > "2022-07-31"
		GROUP BY voucher_no
		ORDER BY TIMESTAMP(posting_date,posting_time) """)
	
	if len(list_voucher) > 0:
		frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE docstatus = 1 AND is_cancelled = 0 AND posting_date > "2022-07-31" """)

	for row in list_voucher:
		repair_gl_entry_tanpa_repost(row[0],row[1])
		print("{}={}".format(row[0],row[1]))
		frappe.db.commit()

@frappe.whitelist()
def repair_gl_entry_tanpa_repost(doctype,docname):
	
	docu = frappe.get_doc(doctype, docname)	
	if doctype == "Stock Entry":
		if docu.purpose == "Material Transfer":
			docu.calculate_rate_and_amount()
			for row in docu.items:
				row.db_update()

			docu.db_update()

	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 1 WHERE `field` = "allow_negative_stock" """)
	docu.update_stock_ledger()
	docu.make_gl_entries()
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 0 WHERE `field` = "allow_negative_stock" """)

@frappe.whitelist()
def repair_gl_entry(doctype,docname):
	
	docu = frappe.get_doc(doctype, docname)	
	delete_sl = frappe.db.sql(""" DELETE FROM `tabStock Ledger Entry` WHERE voucher_no = "{}" """.format(docname))
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 1 WHERE `field` = "allow_negative_stock" """)
	docu.update_stock_ledger()
	docu.make_gl_entries()
	docu.repost_future_sle_and_gle()
	frappe.db.sql(""" UPDATE `tabSingles` SET VALUE = 0 WHERE `field` = "allow_negative_stock" """)

@frappe.whitelist()
def repair_gl_entry_tanpa_stock(doctype,docname):
	docu = frappe.get_doc(doctype, docname)	
	print(docu.name, ' xxx')
	delete_gl = frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(docname))
	docu.make_gl_entries()
	