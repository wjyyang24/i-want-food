import json
import requests
import cgi
import cgitb
cgitb.enable()
print("Content-Type: text/html\n\n")
API_KEY = open("apikey.txt","r").readlines()[0]

args=cgi.parse()
placeID = args["placeID"][0]
print(placeID)