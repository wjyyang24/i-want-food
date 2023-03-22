# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Format for Restauraunt is Description, Budget, DayOpen, DayClose, EndOpen, EndClose, Lat, Long
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

def checkbudget(initialList, maxBudget):
    validPlaces = []
    for place in initialList:
        if place[2] <= maxBudget:
            validPlaces.append(place)
    return validPlaces

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

def checkDistance(initialList, maxDistance, index):
    validPlaces = []
    distance = 0.0
    for place in initialList:
        distance = abs(place[7]-Anchors[index][0]) + abs(place[8]-Anchors[index][1])
        distance = distance*68.706
        if distance < maxDistance:
            validPlaces.append(place)
    return validPlaces

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
print("Welcome to the earliest version of the I Want Food Program! Thank you for trying me out!")

while True:
    try:
        num = float(input("First, what is your budget today? "))
    except ValueError:
        print("You didn't enter a number!")
        continue
    if (num > 0):
        break
    else:
        print("The budget can't be negative!")
Budget = num
#print("The Budget is:", Budget)

while True:
    try:
        num = float(input("Next, what time do you plan on arriving? Please use military + decimal time! EX) 10:30 pm would be 22.5 "))
    except ValueError:
        print("You didn't enter a number!")
        continue
    if (num >= 0 and num <= 24):
        break
    else:
        print("Invalid time!")
Time = num
#print("The Time is:", Time)

flag = True
while flag:
    input_value = input("Do you plan on going on a weekend? Please type 'Y' or 'N'! ")
    if (input_value == "Y" or input_value == "N"):
        if (input_value == "Y"):
            WeekendOrNot = True
        else:
            WeekendOrNot = False
        flag = False
    else:
        print("Sorry, that didn't work. Can you please try again? ")
#print("The Weekend flag is:", WeekendOrNot)

flag = True
while flag:
    input_value = input("Do you plan on traveling from the Willy T '0' or the Student Center '1' ")
    if (input_value == "0" or input_value == "1"):
        flag = False
    else:
        print("Sorry, that didn't work. Can you please try again? ")
AnchorIndex = int(input_value)
#print("The Anchor Index is:", AnchorIndex)

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
#print("The Distance is:", Miles)

valid = checkbudget(Restaurants, Budget)
valid2 = checkHours(valid, Time, WeekendOrNot)
valid3 = checkDistance(valid2, Miles, AnchorIndex)
print("The Valid Restaurants are: ")
placeIndex = 0
for place in valid3:
    print("Location ", placeIndex, ": ", place[0])
    placeIndex += 1

Flag2 = True
while Flag2:
    try:
        input_value = int(input("Would you like to learn more info about any of the restaurants? Type in its index for more info, or '-1' to quit. "))
    except ValueError:
        print("You didn't enter an integer!")
        continue
    if input_value < len(valid3) and input_value >= 0:
        print(valid3[input_value][1])
    elif input_value == -1:
        Flag2 = False
    else:
        print("Invalid Index!")
print("Thank you for using I Want Food! v0.1.2")
