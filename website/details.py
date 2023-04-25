#!/usr/bin/python3.10
import json
import requests
import cgi
import cgitb
def placeDetails(placeID):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={placeID}&key={API_KEY}"
    response = requests.request("GET", url,)
    results = response.text

    return results

cgitb.enable()
print("Content-Type: application/json\n\n")
API_KEY = open("apiKey.txt","r").readlines()[0]

args=cgi.parse()
placeID = args["placeid"][0]

details = placeDetails(placeID)
print(details)