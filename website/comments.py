#!/usr/bin/python3.10
from _csv import reader
import csv
import cgi
import cgitb

FILENAME = "website/restaurants.csv"
def load_csv(filename):
    data = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file, delimiter=",")
        for row in csv_reader:
            if not row:
                continue
            data.append(row)
    return data

def load_csv2(filename):
    data = list()
    with open(filename, 'r+') as file:
        csv_reader = reader(file, delimiter=",")
        for row in csv_reader:
            if not row:
                continue
            data.append(row)
    return data

def readReviews(restName):
    data = load_csv(FILENAME)
    #print(data)
    flag = False
    for row in data:
        if (row[0] == restName):
            for i in range(len(row)-1):
                print(row[i+1])
            flag = True
    if flag == False:
        print("No reviews!")

def writeReview(restName, review):
    data = load_csv2(FILENAME)
    flag = False
    for row in data:
        if (row[0] == restName):
            row.append(review)
            flag = True
    if flag == False:
        data.append([restName, review])
    #print(data)
    with open(FILENAME, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)

cgitb.enable()
print("Content-Type: text/html\n\n")
args=cgi.parse()
placeID = "ChIJ2bonnqtcQogR5WWT3D4UWqQ"#args["placeid"][0]

reviews = readReviews(placeID)