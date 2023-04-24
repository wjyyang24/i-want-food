import json
import time
import requests

WillyT = [38.03315024, -84.50173051]
SC = [38.03987827, -84.50295523]
Anchors = [WillyT, SC]

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


# calls nearbySearch as many times as possible using pagetoken and returns a dictionary of results
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


# check if given location is within the budget
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


# prints description of the specified location
def printInfo(locations, index):
    location = {}
    for i in locations:
        if locations[i].get("placeIndex") == index:
            location = locations[i]
    try: 
        print(f"""
========== {location.get("name")} ==========
{"Open Now" if location.get("opening_hours").get("open_now") == True else "CLOSED"}
Address: {location.get("vicinity")}
Rating: {location.get("rating")} Stars
Price Level: {getPriceInDollarSigns(location.get("price_level"))}
        """)
    except:
        print(f"""
=========================
No info for this location
=========================
        """)


# checks if API_KEY is valid
def checkAPIKEY(API_KEY):
    results = nearbySearch(0, 0, 1, API_KEY, None)
    if results["status"] == "OK" or results["status"] == "ZERO_RESULTS":
        return True
    else:
        print(f"STATUS: {results['status']}")
        return False


if __name__ == '__main__':
    print("""
==================================================
Welcome to iWantFood! Thank you for trying me out!
==================================================
    """)

    API_KEY = input("Please enter your Google Maps API Key: ")
    while True:
        if checkAPIKEY(API_KEY):
            break
        else:
            API_KEY = input("\nInvalid API Key, please try again: ")

    while True:
        try:
            num = float(input("\nFirst, what is your budget today? Please enter a number from 1 (affordable) to 4 (expensive): "))
        except ValueError:
            print("You didn't enter a number!")
            continue
        if (num > 0) and (num <= 4):
            break
        else:
            print("You didn't enter a number from 1-4!")
    budget = num

    flag = True
    while flag:
        input_value = input("\nDo you plan on traveling from the Willy T '0' or the Student Center '1'? ")
        if (input_value == "0" or input_value == "1"):
            flag = False
        else:
            print("Sorry, that didn't work, please try again")
    AnchorIndex = int(input_value)
    currLocation = Anchors[AnchorIndex]
    currLat, currLong = currLocation[0], currLocation[1]

    while True:
        try:
            num = float(input("\nLastly, how far are you willing to travel (in miles)? "))
        except ValueError:
            print("You didn't enter a number!")
            continue
        if (num > 0):
            break
        else:
            print("The distance can't be negative!")
    Miles = num
    km = Miles * 1.609344
    meters = km * 1000

    print("\nSearching...\n")
    locations = moreNearbySearch(currLat, currLong, meters, API_KEY, budget)

    # List the names of the locations returned by nearby search and if they are open
    print("=================== RESULTS ===================")
    placeIndex = 0
    for i in locations:
        try:
            print(f"Location {placeIndex}: {locations[i].get('name')} ({'Open now' if locations[i].get('opening_hours').get('open_now') == True else 'CLOSED'})")
            locations[i]["placeIndex"] = placeIndex
            placeIndex += 1
        except:
            # add flag to location so that printInfo doesn't blow up
            locations[i]["canPrintInfo"] = False

    print()
    Flag2 = True
    while Flag2:
        try:
            input_value = int(input("Would you like to learn more info about any of the restaurants? Type in its location number for more info, or '-1' to quit: "))
        except ValueError:
            print("You didn't enter an integer!")
            continue
        if input_value <= placeIndex and input_value >= 0:
            printInfo(locations, input_value)
        elif input_value == -1:
            Flag2 = False
        else:
            print("Invalid Index!")

    print("Thank you for using I Want Food! v0.3.0")