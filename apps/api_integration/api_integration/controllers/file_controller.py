import frappe

from frappe.utils.file_manager import upload, save_file,write_file

from frappe.model.document import Document

from frappe.utils import cstr
import os
import PIL
from PIL import Image
import base64
from io import BytesIO

from frappe.model.document import Document

# Ini untuk File
# class FileController(Document):
def get_file_settings():
    doc_file_settings = frappe.get_single("File Settings")
    return doc_file_settings

def generate_thumbnail(filename, doctype, name):
    # generate thumbnail using Image PIL
    try:
        is_private = 0
        check_extension = False
        if ".png" in filename:
            check_extension = True
        elif ".jpg" in filename:
            check_extension = True
        elif ".jpeg" in filename:
            check_extension = True
        if check_extension == False:
            return
        doc_file_settings = get_file_settings()
        if doc_file_settings.get("using_file_compression") == 1:
            optimum_width = doc_file_settings.get("file_max_width",0)
            optimum_height = doc_file_settings.get("file_max_height",0)

            # Sitename for generate what site
            sitename = cstr(frappe.local.site)
            cd = os.getcwd()
            name_file_only = filename.replace("/files","").replace("/private","").replace("/","")

            # Getting Image
            if 'private' not in filename:
                img = Image.open(os.path.join(cd,sitename,'public/') + filename)
                # with open(os.path.join(cd,sitename,'public/') + filename, 'rb') as f:
                # 	img = f.read()
            else:
                is_private = 1
                if filename:
                    if filename[0] == "/":
                        img = Image.open(os.path.join(cd,sitename) + filename)
                    else:
                        img = Image.open(os.path.join(cd,sitename,'/') + filename)
                # with open(os.path.join(cd,sitename,'/') + filename, 'rb') as f:
                # 	img = f.read()
            width, height =img.size
            new_width, new_height = generate_new_width_height(width, height,optimum_width,optimum_height)
            # if width<basewidth:
            # 	basewidth = width
            # else:
            # 	if basewidth < width/3:
            # 		basewidth = width/3

            # new_size = 


            # Converting Image
            if ".png" in filename.lower():
                img = img.convert('RGBA')
                # hsize = self.get_height(width, height, optimum_width)

                # if hsize == height:
                #     optimum_width = width
                # img = img.resize((optimum_width, hsize), PIL.Image.ANTIALIAS)
                img = img.resize((int(new_width), int(new_height)), PIL.Image.ANTIALIAS)
                buffered = BytesIO()
                img.save(buffered,format="PNG", quality=100)
                img_str = base64.b64encode(buffered.getvalue())
            else:
                img = img.convert('RGB')
                # hsize = self.get_height(width, height, optimum_width)
                
                # if hsize == height:
                #     optimum_width = width
                img = img.resize((int(new_width), int(new_height)), PIL.Image.ANTIALIAS)
                buffered = BytesIO()
                img.save(buffered,format="JPEG", quality=100)
                img_str = base64.b64encode(buffered.getvalue())
            
            
            true_path_url = sitename+filename
            # print(true_path_url)
            response = {}
            # print(img_str[:10])
            uploaded = write_file(buffered.getvalue(),name_file_only,is_private=is_private)
            # print(uploaded)
            frappe.db.commit()
    except:
        frappe.log_error(frappe.get_traceback(),"Error: Generate Thumbnail")

def generate_new_width_height(width,height,optimum_height,optimum_width):
    if optimum_height != 0:
        if optimum_height > height:
            new_width = width
            optimum_height = height
        else:
            new_width = get_width(width, height, optimum_height)
        return new_width, optimum_width
    elif optimum_width != 0:
        if optimum_width > width:
            new_height = height
            optimum_width = width
        else:
            new_height = get_height(width, height, optimum_width)
        return optimum_width, new_height
    else:
        return width,height
    


def get_height(width,height, optimum_width):
    percentage = (optimum_width / float(width))
    hsize = int((float(height) * min(1.0,float(percentage))))
    return hsize

def get_width(width,height, optimum_height):
    percentage = (optimum_height / float(height))
    wsize = int((float(width) * min(1.0,float(percentage))))
    return wsize

# --------- HOOKS -------------

def generate_thumbnail_hooks(self,method):
    if self.file_url and self.attached_to_doctype and self.attached_to_name:
        generate_thumbnail(self.file_url, self.attached_to_doctype, self.attached_to_name)
