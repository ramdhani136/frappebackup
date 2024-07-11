from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'batch_api_log',
		# 'non_standard_fieldnames': {
		# 	'Delivery Note': 'against_sales_invoice',
		# 	'Journal Entry': 'reference_name',
		# 	'Payment Entry': 'reference_name',
		# 	'Payment Request': 'reference_name',
		# 	'Sales Invoice': 'return_against',
		# 	'Auto Repeat': 'reference_document',
		# },
		# 'internal_links': {
		# 	'Sales Order': ['items', 'sales_order']
		# },
		'transactions': [
			{
				'label': _('Batches'),
				'items': ['API Log']
			}
		]
	}
