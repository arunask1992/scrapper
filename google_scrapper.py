
from bottle import route, run
import requests
import code
from pyquery import PyQuery
from newspaper import Article
import csv
import urllib2
import json
import sys
import pycps
import nltk
import csv

nltk.download('punkt')

result = []
crime_map = {}
start = "/url?q="
end = "&"
final1 = []

@route('/build_accident_dataset')
def crimes():
    with open("text", "w") as outfile:
        pruneDataSet()
        for i in range(0,10):
            scrap(i)
        print("=================================================")
        groupByArea([x for x in final1 if x is not None])
        rest_json = constructJson(crime_map)
        print(rest_json)
        json.dump(rest_json, outfile, indent=4)
        return rest_json


def constructJson(crime_map):
	rest_json = []
	for map in crime_map:
		temp = {}
		temp["name"] = map
		print(map)
		latLong = getLatLong(map).split(',')
		if len(latLong) > 0:
			temp["lattitude"] = latLong[0]
			temp["longitude"] = latLong[1]
		temp["sambavams"] = crime_map[map]
		rest_json.append(temp)
	return json.dumps(rest_json)

def groupByArea(final_crimes):
	for crime in final_crimes:
		if crime in crime_map:
			crime_map[crime] += 1
		else:
			crime_map[crime] = 0

def scrap(index):
	base_url = "https://www.google.co.in/search?q=chennai%20accidents&tbm=nws&start="+str(index)
	web_page = requests.get(base_url, verify=False)
	parsed_content = PyQuery(web_page.text)
	all_crimes = parsed_content('a')
	for crime in all_crimes:
		crime_url = crime.attrib["href"]
		if '/url?q=' in crime_url:
			try:
				article = Article((crime_url.split(start))[1].split(end)[0])
				article.download()
				article.parse()
				article.nlp()
				keywords = article.keywords
				area_name = findLocation(keywords)
				final1.append(area_name)
				area_name = findLocation(article.summary)
				final1.append(area_name)
			except Exception:
				pass

def pruneDataSet():
	with open('areas1.csv', 'rt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		print spamreader
		for row in spamreader:
			result.append(str(row[0]).lower())

def findLocation(keywords):
	for key in keywords:
		for res in result:
			for word in res.split():
				if key == word:
					return res

def getLatLong(area):
	with open('areas1.csv', 'rt') as csvfile:
    		reader = csv.reader(csvfile, delimiter=',')
    		for row in reader:
    		    if row[0] == area:
		            latLong = str(row['latitude']) + "," + str(row['longitude'])
	            return latLong

@route('/lat_long')
def writeLatLong():
    with open('areas.csv', 'rb') as f:
        reader = csv.reader(f)
        areas_list = list(reader)
    with open('areas1.csv', 'w') as csv_file:
        fieldnames = ['area_name', 'latitude', 'longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for area in areas_list:
            latlong = getLatLong(area[0]).split(',')
            writer.writerow({'area_name': area[0], 'latitude': latlong[0], 'longitude': latlong[1]})

run(host='localhost', port= 8080, debug=True)