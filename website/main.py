#!/usr/bin/python3.10
#python script for heliohost
#all material that is printed is returned, so print statements are commented out
import json
import requests
import cgi
import cgitb
import time
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
def nearbySearch(latitude, longitude, radius, key, pagetoken, type = "restaurant"):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type={type}&key={key}"
    if pagetoken is not None:
        url += f"&pagetoken={pagetoken}"
        time.sleep(2)
    payload, headers = {}, {}

    response = requests.request("GET", url, headers=headers, data=payload)
    results = json.loads(response.text)
    return results

def moreNearbySearch(latitude, longitude, radius, key, budget):
    locations = {}
    results = nearbySearch(latitude, longitude, radius, key, None)
    for location in results.get("results"):
        if checkBudget(location, budget):
            locations[location.get("place_id")] = location

    while "next_page_token" in results:
        results = nearbySearch(latitude, longitude, radius, key, results.get("next_page_token"))
        for location in results.get("results"):
            if checkBudget(location, budget):
                locations[location.get("place_id")] = location
    return locations



def checkBudget(location, budget):
    if location.get("price_level") is None:
        return False
    elif location.get("price_level") <= budget:
        return True
    else:
        return False

# translates the priceLevel into Google Maps dollar sign notation
def getPriceInDollarSigns(priceLevel):
    if priceLevel == 1:
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
    location = {}
    for i in locations:
        if locations[i].get("placeIndex") == index:
            location = locations[i]
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
    
    results = moreNearbySearch(currLat, currLong, meters, API_KEY, budget)
    locations = results["results"]

    # List the names of the locations returned by nearby search and if they are open
    #print("The Valid Restaurants are: ")

    placeIndex = 0
    for i in range(len(locations)):
        printInfo(locations,i)
        placeIndex += 1