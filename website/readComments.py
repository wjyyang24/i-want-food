#!/usr/bin/python3.10
import cgi
import cgitb
import comments

cgitb.enable()
print("Content-Type: text/html\n\n")
args=cgi.parse()
placeID = args["placeid"][0]

reviews = comments.readReviews(placeID)