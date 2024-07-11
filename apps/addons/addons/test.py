# -*- coding: utf-8 -*-
# Copyright (c) 2015, erpx and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from addons.frappeclient import FrappeClient
import json
import os
import requests
import subprocess
from frappe.utils.background_jobs import enqueue
from frappe.utils.password import check_password,get_decrypted_password
from frappe.utils import get_site_name

class SyncServerSettings(Document):
	pass


@frappe.whitelist()
def en_call_sync_stock_entry_to_branch(doc,method):
	pass

@frappe.whitelist()
def test_connection():
	print("http://etm.digitalasiasolusindo.com/")
	clientroot = FrappeClient("http://etm.digitalasiasolusindo.com/","administrator","j&3Pmt@7FqdXV5$t")


@frappe.whitelist()
def patch_item():
	list_item = frappe.db.sql(""" 

		SELECT ti.name, ti.item_name, ti.image, tf.`name`, tf.`file_name`, tf.`file_url`, tf.`folder`,
CONCAT(TRIM(ti.item_name),".jpg")
		FROM `tabItem` ti
		 JOIN `tabFile` tf ON CONCAT(ti.item_name,".jpg") = tf.`file_name`
		AND tf.`folder` LIKE "%Reupload%"
		WHERE ti.name IN ("1101302300(32)",
"1103500000",
"1201800100(04)",
"1203503100",
"1400500300(07)",
"1400700200(05)",
"1400800200(12)",
"1401502900(34)",
"1401603800(30)",
"1500100112",
"1501300302",
"1600000000",
"1600200105",
"1600300110",
"1600400210",
"1600500210",
"1600600110",
"1600701710",
"1600800105",
"1600800405",
"1700004400",
"180201300(45)",
"180211300(45)",
"1901000-1807-3",
"1901700-BT956-C-14",
"1902012-5641-10",
"1902702-2182",
"1902703-2182",
"1902712-2182",
"1903002E-3197",
"1903002E-3242",
"1903002E-3243",
"1903302-510091",
"1903303-510091",
"1903312-610081",
"1903312-910057",
"1903602-3181",
"1903603-3181",
"1903612-3181",
"1903802-34",
"1903803-34",
"1903939",
"1903940",
"1904000-297",
"19043-4099",
"1904302-5S",
"1904302-6004",
"1904303-4037",
"1904305-6093",
"1904307A-6093",
"1904311G-03S",
"1904311G-4099",
"1904312-341",
"1904312-9390",
"1904401-4068",
"1904402-04182-33",
"1904402-284",
"1904402-6004",
"1904402-6169-32",
"1904402-9422",
"1904402E-6010",
"1904403-4068",
"1904403-4099",
"1904403-5027",
"1904403-6169",
"1904403-734",
"1904403-9422",
"1904410-01232",
"1904412-284",
"1904412-3210-30",
"1904412B-4068",
"1907602-3210-30",
"1907603-3210-30",
"201401312R-420026",
"2100200100",
"2100400400",
"2100406100",
"2100406200",
"2102002406-H45I",
"2205701200",
"2205701400",
"2205701500",
"2205701700",
"2401010500(66)") 
		 
		AND (image IS NULL OR image = "")
	 """)

	for row in list_item:
		item = frappe.get_doc("Item", row[0])
		item.image = row[5]
		item.db_update()

		print(item.name)
