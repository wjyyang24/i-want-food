import json
import requests

McDonalds = ["McDonalds", "Fast Food", 5, 6, 23, 6, 23, 38.0424713, -84.50286613]
RaisingCanes = ["Raising Canes", "Fast Food", 10, 10, 23, 10, 24, 38.0429525, -84.50421929]
WasabiBarandGrill = ["Wasabi Bar and Grill", "Sushi", 15, 11, 21, 11, 22, 38.04358123, -84.50133363]
CookOut = ["Cook-Out","Fast Food", 8, 11.5, 3, 11.5, 4, 38.04054075, -84.51358787]
BourbonNToulouse = ["Bourbon 'N Toulouse","Cajun", 15, 11, 22, 11, 22, 38.03086996, -84.49104708]
JimmyJohns = ["Jimmy Johns", "Sandwiches", 10, 10.5, 1, 10.5, 1, 38.03298376, -84.4937443]
RollingOven = ["Rolling Oven", "Pizza", 4, 10, 2, 12, 12, 38.04213077, -84.50437168]
Starbucks = ["Starbucks", "Coffee", 8, 6.5, 14.5, 12, 12, 38.03915567, -84.51431934]

Restaurants = [McDonalds, RaisingCanes, WasabiBarandGrill, CookOut, BourbonNToulouse, JimmyJohns, RollingOven, Starbucks]

WillyT = [38.03315024, -84.50173051]
SC = [38.03987827, -84.50295523]
Anchors = [WillyT, SC]

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

"""
def checkHours(initialList, time, endFlag):
    validPlaces = []
    for place in initialList:
        if endFlag == True:
            if place[6] > place[5]: #if closes at pm
                if time > place[5] and time < place[6]:
                    validPlaces.append(place)
            else:
                if time > place[5] or time < place[6]:
                    validPlaces.append(place)
        else:
            if place[4] > place[3]: #if closes at pm
                if time > place[3] and time < place[4]:
                    validPlaces.append(place)
            else:
                if time > place[3] or time < place[4]:
                    validPlaces.append(place)
    return validPlaces
 """


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

    API_KEY = input("Please enter your Google Maps API Key: ")
    print(API_KEY)
    while True:
        if checkAPIKEY(API_KEY):
            break
        else:
            API_KEY = input("Invalid API Key, please try again: ")

    while True:
        try:
            num = float(input("First, what is your budget today? Please enter a number from 1 (affordable) to 4 (expensive): "))
        except ValueError:
            print("You didn't enter a number!")
            continue
        if (num > 0) and (num <= 4):
            break
        else:
            print("You didn't enter a number from 1-4!")
    budget = num
    print("The Budget is:", budget)

    flag = True
    while flag:
        input_value = input("Do you plan on traveling from the Willy T '0' or the Student Center '1' ")
        if (input_value == "0" or input_value == "1"):
            flag = False
        else:
            print("Sorry, that didn't work. Can you please try again? ")
    AnchorIndex = int(input_value)
    currLocation = Anchors[AnchorIndex]
    currLat, currLong = currLocation[0], currLocation[1]

    while True:
        try:
            num = float(input("Lastly, how far are you willing to travel (in miles) "))
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
