
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    import random, string
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_password(doctype,name,fieldname):
	'''
	Untuk mengambil password
	'''
	from frappe.utils.password import get_decrypted_password
	d_password = get_decrypted_password(doctype, name, fieldname=fieldname, raise_exception=False)
	return d_password

def md5encrypt(somestring):
	import hashlib
	m = hashlib.md5()
	m.update(somestring.encode('utf-8'))
	return m.hexdigest()

def sha1encrypt(somestring):
	import hashlib
	m = hashlib.sha1()
	m.update(somestring.encode('utf-8'))
	return m.hexdigest()
