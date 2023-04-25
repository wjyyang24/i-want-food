#!/usr/bin/python3.10
from _csv import reader
import csv

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
    filename = 'Restauraunts.csv'
    data = load_csv(filename)
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
    filename = 'Restauraunts.csv'
    data = load_csv2(filename)
    flag = False
    for row in data:
        if (row[0] == restName):
            row.append(review)
            flag = True
    if flag == False:
        data.append([restName, review])
    #print(data)
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)