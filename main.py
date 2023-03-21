# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Format for Restauraunt is Description, Budget, DayOpen, DayClose, EndOpen, EndClose, Lat, Long
McDonalds = ["McDonalds", "Fast Food", 5, 6, 23, 6, 23]
RaisingCanes = ["Raising Canes", "Fast Food", 10, 10, 23, 10, 24]
WasabiBarandGrill = ["Wasabi Bar and Grill", "Sushi", 15, 11, 21, 11, 22]
CookOut = ["Cook-Out","Fast Food", 8, 11.5, 3, 11.5, 4]
BourbonNToulouse = ["Bourbon 'N Toulouse","Cajun", 15, 11, 22, 11, 22]
JimmyJohns = ["Jimmy Johns", "Sandwiches", 10, 10.5, 1, 10.5, 1]
RollingOven = ["Rolling Oven", "Pizza", 4, 10, 2, 12, 12]
Starbucks = ["Starbucks", "Coffee", 8, 6.5, 14.5, 12, 12]

Restaraunts = [McDonalds, RaisingCanes, WasabiBarandGrill, CookOut, BourbonNToulouse, JimmyJohns, RollingOven, Starbucks]

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



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    valid = checkbudget(Restaraunts, 10)
    valid2 = checkHours(valid, 23.5, False)
    print("The Valid Restauraunts are: ")
    for place in valid2:
        print(place[0])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
