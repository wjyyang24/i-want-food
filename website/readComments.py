#!/usr/bin/python3.10
import cgi
import cgitb
import comments
import json

cgitb.enable()
print("Content-Type: application/json\n\n")
args=cgi.parse()
placeID = args["placeid"][0]

reviews = comments.readReviews(placeID)
print(reviews)