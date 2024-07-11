from __future__ import unicode_literals
import frappe
from frappe.utils import flt, comma_or, nowdate, getdate
from frappe import _
from frappe.model.document import Document
from erpnext.controllers.status_updater import StatusUpdater

@frappe.whitelist()
def overwrite_status_updater(doc,method):
	StatusUpdater.validate_qty = validate_qty2

	for i in doc.items:
		# frappe.throw(i.item_code)
		if i.batal_kirim == 1:
			frappe.throw("Item "+i.item_code+" Melakukan batal Kirim silahkan hapus terlebih dahulu untuk melanjutkan !")

def validate_qty2(self):
	"""Validates qty at row level"""
	self.item_allowance = {}
	self.global_qty_allowance = None
	self.global_amount_allowance = None

	if self.doctype == "Delivery Note" or self.doctype == "Sales Invoice":
		self.global_qty_allowance = flt(frappe.db.get_single_value('Stock Settings', 'over_delivery_allowance'))


	for args in self.status_updater:
		if "target_ref_field" not in args:
			# if target_ref_field is not specified, the programmer does not want to validate qty / amount
			continue

		# get unique transactions to update
		for d in self.get_all_children():
			if hasattr(d, 'qty') and d.qty < 0 and not self.get('is_return'):
				frappe.throw(_("For an item {0}, quantity must be positive number").format(d.item_code))

			if hasattr(d, 'qty') and d.qty > 0 and self.get('is_return'):
				frappe.throw(_("For an item {0}, quantity must be negative number").format(d.item_code))

			if d.doctype == args['source_dt'] and d.get(args["join_field"]):
				args['name'] = d.get(args['join_field'])

				# get all qty where qty > target_field
				item = frappe.db.sql("""select item_code, `{target_ref_field}`,
					`{target_field}`, parenttype, parent from `tab{target_dt}`
					where `{target_ref_field}` < `{target_field}`
					and name=%s and docstatus=1""".format(**args),
					args['name'], as_dict=1)
				if item:
					item = item[0]
					item['idx'] = d.idx
					item['target_ref_field'] = args['target_ref_field'].replace('_', ' ')

					# if not item[args['target_ref_field']]:
					# 	msgprint(_("Note: System will not check over-delivery and over-booking for Item {0} as quantity or amount is 0").format(item.item_code))
					if args.get('no_allowance'):
						item['reduce_by'] = item[args['target_field']] - item[args['target_ref_field']]
						if item['reduce_by'] > .01:
							self.limits_crossed_error(args, item, "qty")

					elif item[args['target_ref_field']]:
						if self.doctype != "Delivery Note" and self.doctype != "Sales Invoice":
							self.check_overflow_with_allowance(item, args)


	# frappe.throw("test")