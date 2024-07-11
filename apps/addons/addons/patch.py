from __future__ import unicode_literals
import frappe
import pandas as pd


# patch sinv account n repair gl entries
@frappe.whitelist()
def sinv_account():
    col = ["Name", "Item", "Incoming_Account"]
    data = pd.read_excel (r'/home/frappe/frappe-bench/apps/addons/addons/sinv_account.xls') 
    df = pd.DataFrame(data, columns=col)
    
    for index, row in df.iterrows():
        #Sales Invoice
        doc_si = frappe.get_doc('Sales Invoice Item',{ 'parent':row['Name'], 'item_code': row['Item']})
        if not pd.isna(row['Incoming_Account']):
            doc_si.income_account = row['Incoming_Account']
        doc_si.db_update()
        print("Item {} pada doc {} berhasil di rubah".format(row['Item'], row['Name']))

        frappe.db.sql(""" DELETE FROM `tabGL Entry` WHERE voucher_no = "{}" """.format(row['Name']))
        docu = frappe.get_doc('Sales Invoice', row['Name'])	
        docu.make_gl_entries()
        docu.repost_future_sle_and_gle()

