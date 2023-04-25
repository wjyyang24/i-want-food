#!/usr/bin/python3.10
import cgi
import cgitb
import comments

cgitb.enable()
print("Content-Type: text/html\n\n")

args=cgi.parse()
if len(args) == 0:
    placeID = input("Enter place ID: ")
else:
    placeID = args["placeid"][0]

comments.readReviews(placeID)