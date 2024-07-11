import frappe
from frappe.model.document import Document
from frappe import _


@frappe.whitelist(allow_guest=False)
def generate_qr_code(prec=None):
    if prec == "" or prec == None:
        frappe.throw(_("Purchase Receipt tidak ditemukan"))
    else:
        pass

    prec_doc = frappe.get_doc('Purchase Receipt', prec)
    items = prec_doc.items

    # filter items yang akan di generate QR nya saja
    items_filtered = []
    for item in items:
        if item.quantity_of_items_per_qr_code > 0:
            items_filtered.append(item)
        else:
            # Tidak akan di generate
            pass

    # Generate QR nya dengan cara buat dt
    import math
    for item in items_filtered:
        quantity_of_items_per_qr_code = item.quantity_of_items_per_qr_code
        accepted_qty = item.qty
        item_name = item.item_code
        uom_packing = frappe.db.get_value('Item', item_name, 'uom_packing')
        if uom_packing == "" or uom_packing == None:
            frappe.throw(
                _("Silahkan isi uom packing terlebih dahulu di doctype item.<br> ID Barang: {}".format(item_name)))

        range_buat_qr_code = math.ceil(
            accepted_qty / quantity_of_items_per_qr_code)
        for idx in range(range_buat_qr_code):
            doc = frappe.new_doc('Registration Packing ID')
            doc.purchase_receipt = prec
            doc.item = item_name
            doc.uom_packing = uom_packing
            if idx + 1 == range_buat_qr_code:
                qty_last = accepted_qty % quantity_of_items_per_qr_code
                if qty_last == 0 :
                    qty_last = quantity_of_items_per_qr_code
                doc.conversion = qty_last
            else:
                doc.conversion = quantity_of_items_per_qr_code
            doc.insert()
            print("{} => {} => {}".format(doc.name, item_name, doc.conversion))

    # Jika sudah berhasil terbuat semua maka commit
    frappe.db.commit()
