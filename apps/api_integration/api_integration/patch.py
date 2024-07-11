import datetime
import requests

def get_all_point_from_api():
	clno = 1
	clno_till = 254000
	f = open("get_all_point_from_api.txt", "a")
	f.write("Today: {}\n".format(str(datetime.datetime.now())))
	f.write("CLNO FROM: {} sampai {}\n".format(str(clno),str(clno_till)))
	f.write("clno,point,status\n")
	for i in range(clno,clno_till):
		request_param = {'clno': i}
		r = requests.post("http://pointplus.ciputramall.com/system/api/cek_point.php", data=request_param)
		print("clno : "+str(i))
		# print(r)
		res = r.json()
		if res["clno"]:
			f.write(res["clno"]+","+res["point"])
			if int(res["point"]) < 0:
				f.write(","+"minus"+"\n")
			else:
				f.write("\n")
	f.close()