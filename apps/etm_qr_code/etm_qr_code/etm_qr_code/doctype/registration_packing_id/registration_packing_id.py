# Copyright (c) 2022, DAS DEV and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RegistrationPackingID(Document):
    show_print_qr_alert = False

    def before_save(self):
        global show_print_qr_alert
        show_print_qr_alert = False
        self.id_packing = self.name
        qr = self.qr_code
        if qr == None or qr == '':
            self.qr_code = self.generate_and_save_qr_also_return_path()
            frappe.set_value("Item", self.item, {
                "is_use_qr_code": 1
            })
        else:
            # Generate untuk mengupdate CONVERSION
            # Field yang bisa di edit hanya CONVERSION jika is_in nya belum check
            # Sehingga hanya bisa trigger before_save ketika ada perubahan di CONVERSION
            self.qr_code = self.generate_and_save_qr_also_return_path()
            show_print_qr_alert = True

    def on_change(self):
        # Untuk menghilangkan error dari dt File.
        # Sudah confirmed ke ko bobby tidak apa2 ga save ke dt file.
        frappe.clear_messages()
        global show_print_qr_alert
        if show_print_qr_alert == True:
            frappe.msgprint("Conversion berhasi di update.<br>Silahkan print ulang QR Code untuk update QR Code lama.")

    # End of hooks --------

    """ gilang: Generate QR Code and return Photo Path"""

    def generate_and_save_qr_also_return_path(self):
        import os
        import json
        import qrcode
        from PIL import Image
        # Directory init
        directory_base = '/files/registration-packing-id/'
        directory_full_base = '{}/public{}'.format(
            frappe.get_site_path(), directory_base)
        directory_file = '{}{}/'.format(directory_base, frappe.utils.today())
        directory_full = '{}/public{}'.format(
            frappe.get_site_path(), directory_file)
        directory_file_with_file_name = '{}{}.png'.format(
            directory_file, self.name)
        directory_full_with_file_name = '{}{}.png'.format(
            directory_full, self.name)

        # Check is directory base valid
        # Jika tidak valid maka buat directory base
        valid = os.path.isdir(directory_full_base)
        if valid == False:
            os.mkdir(directory_full_base)

        # Check is directory tanggal valid
        # Jika tidak valid maka buat directory tanggal
        valid = os.path.isdir(directory_full)
        if valid == False:
            os.mkdir(directory_full)

        # Generate and Save QR ke directory
        json_dict = {
            "id_packing": self.name,
            "item": self.item,
            "item_name": self.item_name,
            "stock_uom": self.stock_uom,
            "uom_packing": self.uom_packing,
            "conversion": self.conversion
        }
        # logo = Image.open("./assets/etm_qr_code/image/logo_bw.jpg")
        # logo = logo.resize((200, 200), Image.ANTIALIAS)
        qr_code = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr_code.add_data(json.dumps(json_dict))
        qr_code.make()
        qr_img = qr_code.make_image(
            fill_color="Black", back_color="white").convert('RGB')
        # pos = ((qr_img.size[0] - logo.size[0]) // 2,
        #        (qr_img.size[1] - logo.size[1]) // 2)
        # qr_img.paste(logo, pos)
        qr_img.save(directory_full_with_file_name)

        # Return path
        return directory_file_with_file_name
