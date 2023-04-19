#!/usr/bin/python3.10
#python script for heliohost
#all material that is printed is returned, so print statements are commented out
import json
import requests
import cgi
import cgitb
cgitb.enable()
print("Content-Type: text/html\n\n") #header for browser reading data
apiFile = open("apiKey.txt","r")
API_KEY = apiFile.readlines()[0]
apiFile.close()
WillyT = [38.03315024, -84.50173051]
SC = [38.03987827, -84.50295523]
Anchors = [WillyT, SC]

args=cgi.parse()
budget = int(args["budget"][0])
AnchorIndex = int(args["anchor"][0])
Miles = float(args["miles"][0])


# use the google maps api nearby search to find 20 results
# returns json string
# radius in meters
def nearbySearch(latitude, longtitude, radius, maxprice, key, type = "restaurant"):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longtitude}&radius={radius}&type={type}&key={key}&maxprice={maxprice}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    results = json.loads(response.text)

    # print(results)
    return results


def checkBudget(initialList, maxBudget):

    validPlaces = []
    for place in initialList["results"]:
        # print(place)
        if place.get('price_level') is not None and place.get('price_level') <= maxBudget:
            validPlaces.append(place["name"])
    return validPlaces


def checkDistance(initialList, maxDistance, index):
    validPlaces = []
    distance = 0.0
    for place in initialList:
        distance = abs(place[7]-Anchors[index][0]) + abs(place[8]-Anchors[index][1])
        distance = distance*68.706
        if distance < maxDistance:
            validPlaces.append(place)
    return validPlaces


def getPriceInDollarSigns(priceLevel):
    if priceLevel == 0:
        return "Free!(?)"
    elif priceLevel == 1:

        return "$"
    elif priceLevel == 2:
        return "$$"
    elif priceLevel == 3:
        return "$$$"
    elif priceLevel == 4:
        return "$$$$"
    else:
        return "No info"


def printInfo(locations, index):
    location = locations[index]
    try:
        print(f"""
        <a href="/cgi-bin/details.html?placeid={location.get("place_id")}">========== {location.get("name")} ==========</a><br>
        {"Open Now" if location.get("opening_hours").get("open_now") == True else "CLOSED"}<br>
        Address: {location.get("vicinity")}<br>
        Rating: {location.get("rating")} Stars<br>
        Price Level: {getPriceInDollarSigns(location.get("price_level"))}<br>
            """)
    except:
        pass

if __name__ == '__main__':
    currLocation = Anchors[AnchorIndex]
    currLat, currLong = currLocation[0], currLocation[1]

    km = Miles * 1.609344
    meters = km * 1000

    #print(f"{currLat}, {currLong}, {km}")
    
    results = nearbySearch(currLat, currLong, meters, budget, API_KEY)
    locations = results["results"]

    # List the names of the locations returned by nearby search and if they are open
    #print("The Valid Restaurants are: ")

    placeIndex = 0
    for i in range(len(locations)):
        printInfo(locations,i)
        placeIndex += 1