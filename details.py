#!/usr/bin/python3.10
import json
import requests
import cgi
import cgitb
cgitb.enable()
print("Content-Type: text/html\n\n")
API_KEY = open("apiKey.txt","r").readlines()[0]

args=cgi.parse()
placeID = args["placeid"][0]
print("test")
print(placeID)