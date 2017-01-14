import csv
import urllib
import json
import sys
import pycps
import nltk
import requests
import code
from bottle import route, run

def getLatLong(area):
	api_key = 'AIzaSyDOjBGZEBvLCpHXkNvl-bBBxKHhzAeSaqU'
	area = area.replace(" ", "%20")
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+area+'%20chennai&key='+api_key
	response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
	if len(response["results"]) > 0:
		co_ord=response["results"][0]["geometry"]["location"]
		latLong = str(co_ord["lat"]) + "," + str(co_ord["lng"])
		return latLong

def writeLatLong():
    with open('areas.csv', 'rb') as f:
        reader = csv.reader(f)
        areas_list = list(reader)
    with open('areas1.csv', 'w') as csv_file:
        fieldnames = ['area_name', 'latitude', 'longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for area in areas_list:
            latLong = getLatLong(area).split(',')
            writer.writerow({'area_name': area, 'latitude': latlong[0], 'longitude': latlong[1]})
