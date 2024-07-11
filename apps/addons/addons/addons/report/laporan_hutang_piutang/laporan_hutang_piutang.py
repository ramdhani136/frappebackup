# Copyright (c) 2013, PT DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	party_type = ""
	if filters.get("account"):
		if frappe.get_doc("Account", filters.get("account")).account_type == "Receivable":
			columns= [
				"Nama Customer:Link/Customer:220",
				"Saldo Awal Piutang:Currency:200",
				"Penambahan:Currency:150",
				"Pengurangan:Currency:150",
				"Saldo Akhir:Currency:200"
			]
			party_type = "Customer"
		elif frappe.get_doc("Account", filters.get("account")).account_type == "Payable":
			columns= [
				"Nama Supplier:Link/Supplier:220",
				"Saldo Awal Hutang:Currency:200",
				"Penambahan:Currency:150",
				"Pengurangan:Currency:150",
				"Saldo Akhir:Currency:200"
			]
			party_type = "Supplier"

		if party_type:
			data_party = frappe.db.sql(""" 
				SELECT party
				FROM `tabGL Entry` WHERE account = "{}"
				GROUP BY party
			""".format(filters.get("account")))

			for row in data_party:
				data_awal = frappe.db.sql(""" 
					SELECT IFNULL(SUM(IFNULL(debit,0)-IFNULL(credit,0)),0), party
					FROM `tabGL Entry` WHERE account = "{}" AND posting_date < "{}"
					and party = "{}"
					and is_cancelled = 0
					and docstatus = 1
					GROUP BY party
				""".format(filters.get("account"), filters.get("from_date"), row[0]))

				data_debit = frappe.db.sql(""" 
					SELECT IFNULL(SUM(IFNULL(debit,0)),0) 
					FROM `tabGL Entry` WHERE account = "{}" AND posting_date >= "{}" AND posting_date <= "{}"
					AND party = "{}" AND party_type = "{}"
					and is_cancelled = 0
					and docstatus = 1
				""".format(filters.get("account"), filters.get("from_date"),filters.get("to_date"), row[0], party_type))

				data_credit = frappe.db.sql(""" 
					SELECT IFNULL(SUM(IFNULL(credit,0)),0)
					FROM `tabGL Entry` WHERE account = "{}" AND posting_date >= "{}" AND posting_date <= "{}"
					AND party = "{}" AND party_type = "{}"
					and is_cancelled = 0
					and docstatus = 1
				""".format(filters.get("account"), filters.get("from_date"),filters.get("to_date"), row[0], party_type))

				awal = 0
				masuk = 0 
				keluar = 0
				total = 0

				if len(data_awal)>0:
					if party_type == "Customer":
						awal = data_awal[0][0]
					else:
						awal = data_awal[0][0] * -1

				if len(data_debit)>0:
					if party_type == "Customer":
						masuk = data_debit[0][0]
					else:
						keluar = data_debit[0][0]

				if len(data_credit) > 0:
					if party_type == "Customer":
						keluar = data_credit[0][0]
					else:
						masuk = data_credit[0][0]

				if party_type == "Customer":
					keluar = data_credit[0][0]
				else:
					masuk = data_credit[0][0]

				if party_type == "Customer":
					total = float(awal) + float(masuk) - float(keluar)
				else:
					total = float(awal) + float(masuk) - float(keluar)

				if awal or masuk or keluar:
					data.append([row[0],awal, masuk, keluar, total])

	return columns, data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def account_able_query(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.controllers.queries import get_match_cond

	# income account can be any Credit account,
	# but can also be a Asset account with account_type='Income Account' in special circumstances.
	# Hence the first condition is an "OR"
	if not filters: filters = {}

	condition = ""
	if filters.get("company"):
		condition += "and tabAccount.company = %(company)s"

	return frappe.db.sql("""select tabAccount.name from `tabAccount`
			where (tabAccount.account_type in ("Payable", "Receivable"))
				and tabAccount.is_group=0
				and tabAccount.`{key}` LIKE %(txt)s
				{condition} {match_condition}
			order by idx desc, name"""
			.format(condition=condition, match_condition=get_match_cond(doctype), key=searchfield), {
				'txt': '%' + txt + '%',
				'company': filters.get("company", "")
			})
