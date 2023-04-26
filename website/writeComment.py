#!/usr/bin/python3.10
from csv import reader
import csv
import cgi
import cgitb
import readComments
FILENAME = "comments.csv"

cgitb.enable()
print("Content-Type: text/html\n\n")
FILENAME = "comments.csv"
args=cgi.parse()
placeID = args["placeid"][0]
review = args["review"][0]

readComments.writeReview(placeID,review)