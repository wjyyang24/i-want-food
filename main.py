import json
import requests
from sys import argv
WillyT = [38.03315024, -84.50173051]
SC = [38.03987827, -84.50295523]
Anchors = [WillyT, SC]

budget = argv[1]
AnchorIndex = argv[2]
Miles = argv[3]

# use the google maps api nearby search to find 20 results
# returns json string
# radius in meters
def nearbySearch(latitude, longtitude, radius, key, type = "restaurant"):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longtitude}&radius={radius}&type={type}&key={key}"
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
    location = locations[index]
    print(f"""
========== {location.get("name")} ==========
{"Open Now" if location.get("opening_hours").get("open_now") == True else "CLOSED"}
Address: {location.get("vicinity")}
Rating: {location.get("rating")} Stars
Price Level: {getPriceInDollarSigns(location.get("price_level"))}
    """)


def checkAPIKEY(API_KEY):
    results = nearbySearch(0, 0, 1, API_KEY)
    if results["status"] == "OK" or results["status"] == "ZERO_RESULTS":
        return True
    else:
        print(f"STATUS: {results['status']}")
        return False


if __name__ == '__main__':
    print("Welcome to the earliest version of the I Want Food Program! Thank you for trying me out!")

    API_KEY = "AIzaSyAZCI5CESGptwRNxXKBjMSCmTKfr-pAgic"
    print(API_KEY)
    while True:
        if checkAPIKEY(API_KEY):
            break
        else:
            pass

    print("The Budget is:", budget)


    currLocation = Anchors[AnchorIndex]
    currLat, currLong = currLocation[0], currLocation[1]

    km = Miles * 1.609344
    meters = km * 1000

    print(f"{currLat}, {currLong}, {km}")
    
    results = nearbySearch(currLat, currLong, meters, API_KEY)
    locations = results["results"]

    # List the names of the locations returned by nearby search and if they are open
    print("The Valid Restaurants are: ")
    placeIndex = 0
    for i in locations:
        try:
            print(f"Location {placeIndex}: {i.get('name')} ({'Open now' if i.get('opening_hours').get('open_now') == True else 'CLOSED'})")
        except:
            pass
        placeIndex += 1

    """ # Print restaurant names that are within the inputted budget
    valid = checkBudget(results, budget)
    print(f"\nThere are {len(valid)} open restaurants within your budget")
    for restaurant in valid:
        print(restaurant) """

    Flag2 = True
    while Flag2:
        try:
            input_value = int(input("Would you like to learn more info about any of the restaurants? Type in its index for more info, or '-1' to quit. "))
        except ValueError:
            print("You didn't enter an integer!")
            continue
        if input_value <= placeIndex and input_value >= 0:
            printInfo(locations, input_value)
        elif input_value == -1:
            Flag2 = False
        else:
            print("Invalid Index!")

    print("Thank you for using I Want Food! v0.2.0")
