# MiHive (c) 2014 David Tarrant
# License: GPLv3

import cookielib
import urllib
import urllib2
import json
import os
import time
from datetime import date

# Open config file
json_data=open('/home/pi/MiHive-dev/config.json')

config = json.load(json_data)
json_data.close()

config = config["config"]
username = config[0]["username"]
password = config[1]["password"]
dataPath = config[2]["dataPath"]

def makeRequest(url,payload):
   global urllib2
   global opener
   if payload:
	# Use urllib to encode the payload
	data = urllib.urlencode(payload)
	# Build our Request object (supplying 'data' makes it a POST)
	req = urllib2.Request(url, data)
   else:
	req = urllib2.Request(url)

   # Make the request and read the response
   try:
	resp = urllib2.urlopen(req)
   except urllib2.URLError, e:
	print e.code
   else:
	# 200
	body = resp.read()
	return body;
   return None;

def writeToFile(data):
   global dataPath
   year = date.today().year
   month = date.today().month
   day = date.today().day
   fullpath = dataPath + "/" + str(year) + "/" + str(month).zfill(2);
   file = fullpath + "/" + str(day).zfill(2) + ".json"
   if not os.path.exists(fullpath):
	os.makedirs(fullpath) 

   if os.path.exists(file):
	with open(file, 'a+') as outfile:
		outfile.writelines(",\n")
		json.dump(data, outfile)
   else:
   	with open(file, 'a+') as outfile:
		json.dump(data, outfile)

# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)

url = 'https://www.hivehome.com/login'
payload = {
  'username':username,
  'password':password
  }

# Login
makeRequest(url,payload)

# Get timestamp for record
timeStamp = time.time()

# Get temporature (weather) data for inside and out
opener.addheaders = [('Accept', 'application/json')];
url = 'https://www.hivehome.com/myhive/weather';
body = makeRequest(url,None)
jsonData = json.loads(body)
jsonData['time'] = timeStamp

# Get heating target temporature
opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')];
url = 'https://www.hivehome.com/myhive/heating/target';
body = makeRequest(url,None)
target = json.loads(body)
jsonData['target'] = target['target']

# Get hot water status
url = 'https://www.hivehome.com/myhive/hotwater/schedule';
body = makeRequest(url,None)
water = json.loads(body)
jsonData['hotWater'] = water['current']

writeToFile(jsonData)
