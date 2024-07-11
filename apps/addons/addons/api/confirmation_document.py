# Copyright (c) 2022, PT DAS and contributors
# For license information, please see license.txt

import frappe
import json, sys
from frappe.model.document import Document
from api_integration.validation import success_format, error_format

@frappe.whitelist(allow_guest=False)
def update_child_cd():
    try:
        frappe.db.begin()
        data = json.loads(frappe.request.data.decode('utf-8'))

        # Check field doctype
        if data.get("doctype") == None or data.get("doctype") == "":
            return error_format("Field doctype tidak ditemukan.")
        else:
            if data.get("doctype") == "Confirmation Document":
                pass
            else:
                return error_format("Field doctype harus Confirmation Document.")
        
        # Check field name
        if data.get("name") == None or data.get("name") == "":
            return error_format("Field name tidak ditemukan.")
        else:
            pass

        # Cek apakah dokumen sudah di submit belum
        doc = frappe.get_doc("Confirmation Document",data.get("name"))
        if (doc.docstatus == 1):
            return error_format("Tidak dapat melakukan update, dokumen sudah di submit.")
        else:
            pass
        
        # Update Child Items
        if data.get("items") == None:
            pass
        else:
            # Update child doctype
            for item in data.get("items"):
                item.pop("modified", None)
                update_doc(item)

        # Update Child PR Items
        if data.get("pr_items") == None:
            pass
        else:
            # Update child doctype
            for item in data.get("pr_items"):
                item.pop("modified", None)
                update_doc(item)

        # Update Document
        data.pop("items", None)
        data.pop("pr_items", None)
        data.pop("modified", None)
        update_doc(data)
        
        return success_format(frappe.get_doc("Confirmation Document",data.get("name")))
    except:
        frappe.db.rollback()
        return error_format(exceptions=sys.exc_info(), code=500, err_text="", indicator="red")

def update_doc(post):
    doc = frappe.get_doc(post['doctype'], post['name'])

    update = False
    is_child_doc = frappe.get_value("DocType", post['doctype'], ['istable'])
    if is_child_doc:
        doctype = doc.parenttype
        name = doc.parent
    else:
        doctype = post['doctype']
        name = post['name']

    docshares = frappe.get_all("DocShare", fields="*", filters=[['user', '=', frappe.session.user], ['share_doctype', '=', doctype], ['share_name', '=', name]])
    if len(docshares) > 0:
        for d in docshares:
            if d.write == 1:
                update = True
            else:
                pass
    else:
        update = True

    if update == False:
        return error_format(exceptions=sys.exc_info(), code=500, err_text=_("Insufficient Permission for {doctype}".format(doctype=doctype)), indicator="red")

    doc.update(post)
    doc.save()