import requests
from bs4 import BeautifulSoup
import json
import re
import time

tmp_ip = {}

ip_details = []
ip_list = {}
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
def add_ipdetails(ip,user):
	tmp = {ip:user}
	ip_details.append(tmp)

def add_iplist(ip):
	tmp = {ip:1}
	ip_list.update(tmp)

def add_temp(user):
	tmp = {user:1}
	tmp_ip.update(tmp)

url = "http://changeme.com/login"

s = requests.Session()

resp = s.get(url)
soup = BeautifulSoup(resp.text,'lxml')
nonce = soup.find('input',{'name':'nonce'}).get('value')
param={
	'name':'changeme',
	'password':'changeme',
	'nonce':nonce
}
resp= s.post(url,data=param)
totalcheck = 0
totaluser=95
urluser = "http://changeme.com/admin/users/"
for x in range(0,totaluser+1):
	getdetail = s.get(urluser+str(x))
	resp = getdetail.text

	if '404' not in resp:
		totalcheck += 1
		soup = BeautifulSoup(resp,'lxml')
		name = soup.find('h1',{'id':'team-id'})
		name = name.contents[0]
		#print "[FOUND] - ID {} : {}".format(totalcheck,name)
		table_div = soup.find('div',{'class':'row pt-5'})
		table = table_div.find_all('td',{'class':'text-center'})
		for y in table:
			ip = str(y.contents[0])
			
			check = re.search("^[0-9]", ip)
			if(check):
				add_ipdetails(ip,name)
				add_iplist(ip)
print "[INFO]: Found {} users.".format(totalcheck)
print "[INFO]: Found {} IP.".format(len(ip_list))

for ip in ip_list:
	for details in ip_details:
		getname = details.get(ip,"Kosong")
		if getname != "Kosong":
			add_temp(getname)
	if len(tmp_ip) > 1:
		getisp = requests.get("http://ip-api.com/json/"+str(ip))
		if is_json(getisp.text):
			ispdetails = json.loads(getisp.text)
			if ispdetails['status'] == "success":
					print "[IP] {} - {}".format(ip,ispdetails['isp'])
			else:
					print "[IP] {} - {}".format(ip,ispdetails['message'])
		else:
			print "[IP] {} - {}".format(ip,"API ERROR")
		for test in tmp_ip:
			print "\t[-] {}".format(test)
	tmp_ip.clear()


