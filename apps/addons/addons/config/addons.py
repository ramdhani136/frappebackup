from __future__ import unicode_literals
from frappe import _

def get_data():
	return[
		{
			"label": _("Document"),
			"items":[
				{
					"type": "doctype",
					"name": "Price List Generator",
					"description": _("Price List Generator"),
					"onboard":1,
				},
			]
		},
		{
			"label": _("Reports"),
			"items":[
				{
					"type": "report",
					"name": "Minimum Stock By Item Group",
					"description": _("Minimum Stock By Item Group"),
					"is_query_report": True,
					"onboard":1,
				},
				{
					"type": "report",
					"name": "Laporan Hutang Piutang",
					"description": _("Laporan Hutang Piutang"),
					"is_query_report": True,
					"onboard":1,
				},
				{
					"type": "report",
					"name": "Accounts Receivable with Account Filter",
					"description": _("Accounts Receivable with Account Filter"),
					"is_query_report": True,
					"onboard":1,
				},
			]
		}
	]