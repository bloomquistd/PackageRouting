#Drew Bloomquist
#ID: 011970735
#WGU Email: dbloo17@wgu.edu
#7/30/2024

import csv
import datetime

from HashTable import HashTable
from Package import Package
from Truck import Truck
#High level flow of the program:
#1. Define CSV File functions and extract data into corresponding data structures
#2. Function to find the distance between 2 addresses, then algorithm to find the closest
#   package location.
#3. Trucks deliver the packages based on the function to find the nearest package location.
#   Truck and package information gets updated as each package is delivered.
#4. Menu function and options defined.
#5. Initialize and load trucks, deliver the packages.
#6. Call menu to view delivery information.

def loadPackageData(fileName, myHash):
    # Open csv file and read data, using the "," delimiter to separate elements into a list
    with open(fileName) as packageData:
        packageData = csv.reader(packageData, delimiter=',')
        #Loop through the rows in package data
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pZipcode = package[3]
            pDeadline = package[4]
            pWeight = package[5]
            pNote = package[6]
            pStatus = "At Hub"
            #Initialize/create package object with data from CSV file
            p = Package(pID, pAddress, pCity, pZipcode, pDeadline, pWeight, pNote, pStatus)
            #Add package object to hash table using the ID as the key
            myHash.insert(pID, p)


def loadDistanceData(fileName):
    #Open CSV file, append data in the CSV file to the distance array/list. Mirroring recommended steps
    #in Nearest Neighbor Implementation Steps example on Course Search
    with open(fileName) as distanceData:
        distanceData = csv.reader(distanceData)
        distanceArray = []
        #Loop through the rows in distance data and append the values to the distance array
        for distance in distanceData:
            distanceArray.append(distance)
    return distanceArray


def loadAddressData(fileName):
    #Open CSV file, append data in the CSV file to the distance array/list. Mirroring recommended steps
    #in Nearest Neighbor Implementation Steps example on Course Search
    with open(fileName) as addressData:
        addressData = csv.reader(addressData)
        addressArray = []
        # Loop through the rows in addressData and append the values to the addressArray
        for address in addressData:
            #If you just append address - it's a list in it of itself and
            #you can't compare the address in the package to the address in the list.
            #So you have to look at index 0 to do the string comparisons
            addressArray.append(address[0])
    return addressArray


#Initializing hash table
myHash = HashTable()

#Parsing data from the CSVs
loadPackageData('packageFile.csv', myHash)
distance_array = loadDistanceData('distanceFile.csv')
address_array = loadAddressData('addressFile.csv')


#Takes 2 string addresses and finds the index from the address_array to then
#use as the indices in the distance_array
#Used the suggested method the in Nearest Neighbor Implementation Steps example on Course Search
def distanceBetween(address1, address2):
    distance = distance_array[address_array.index(address1)][address_array.index(address2)]
    #Since the distance table was only half full and the distances are reversible (distance from
    #A to B is equal to the distance from B to A) - if the distance found is null, reverse the
    #order of the addresses in the lookup.
    if distance == "":
        distance = distance_array[address_array.index(address2)][address_array.index(address1)]
    #Have to return a float to do mathematical comparisons/arithmetic
    return float(distance)


#Used Project Implementation Steps - Example Nearest Neighbor on Course search as a guide.
def minDistanceFrom(fromAddress, truckPackages):
    #Set initial minDistance and closest package ID
    minDistance = 1000000
    closestPackageID = truckPackages[0]
    #Loop through every packageID remaining in the truck
    for packageID in truckPackages:
        #find the package in the hash table using packageID
        package = myHash.search(packageID)
        #calculate the distance between where the truck currently is and the
        #package's address
        distance = distanceBetween(fromAddress, package.address)
        #if the distance is less than the current minDistance, set minDistance
        #to the new value and closestPackageID to the packageID we're on
        if distance <= minDistance:
            minDistance = distance
            closestPackageID = packageID
    #return the closest package ID
    return closestPackageID


#Return the desired elements based on packageID
def packageLookup(packageID):
    package = myHash.search(packageID)
    return [package.address, package.deadline, package.city, package.zipcode, package.weight, package.status,
            package.deliveryTime]


#Used Project Implementation Steps - Example Nearest Neighbor on Course search as a guide.
def truckDeliverPackages(truck):
    #Loop through all the packages in the truck to set the package departure time to the
    #truck's departure time
    for packageID in truck.packages:
        package = myHash.search(packageID)
        package.departureTime = truck.departureTime
    #loop through the routing algorithm until there are no packages left on the truck
    while len(truck.packages) > 0:
        #use the minDistance (nearest neighbor algorithm) to determine the next package to be delivered
        nextPackageID = minDistanceFrom(truck.currentLocation, truck.packages)
        #find the package object from the hash table
        package = myHash.search(nextPackageID)
        #add the distance between the package address & the truck's current location
        #to the truck's total driving distance
        truck.distance += distanceBetween(truck.currentLocation, package.address)
        #update package status
        package.status = "Delivered"
        #update package delivery time based on the distance the truck drove at 18 mph and the package's
        #departure time
        package.deliveryTime = datetime.timedelta(hours=truck.distance / 18.0) + package.departureTime

        #update package #9's address at 10:20am
        if package.deliveryTime >= datetime.timedelta(hours=10, minutes=20):
            package9 = myHash.search(9)
            package9.address = "410 S State St"
            package9.city = "Salt Lake City"
            package9.zipcode = 84111
        else:
            package9 = myHash.search(9)
            package9.address = "300 State St"
            package9.city = "Salt Lake City"
            package9.zipcode = 8403
        #Update truck's current location to the package's location
        truck.currentLocation = package.address
        #remove the package from the truck
        truck.packages.remove(nextPackageID)
    #update truck's distance to return to the hub and set the return time based on total distance and
    #the truck's departure time
    truck.distance += distanceBetween(truck.currentLocation, "4001 South 700 East")
    truck.returnTime = datetime.timedelta(hours=truck.distance / 18.0) + truck.departureTime


def main():
    #Loop sets up the initial menu.
    while True:
        #Print menu options
        print('***************************************')
        print('1. Print All Package Status and Total Mileage  ')
        print('2. Get a Single Package Status with a Time')
        print('3. Get All Package Status with a Time ')
        print('4. Exit the Program      ')
        print('***************************************')

        #strip the input to make for easier string comparisons
        menuOption = input("Enter a menu option: ").strip()

        if (menuOption == "1"):
            #Print header
            print("All package statuses and total mileage: ")
            print(
                "Truck ID, PackageID, Address, City, State, Zip, Delivery Deadline, Mass Kg, Notes, Status, Delivery Time, Departure Time")
            #Loop through all package IDs, find the package, and print the data on the package.
            for packageID in range(1, 41):
                #Lookup package by packageID
                package = myHash.search(packageID)
                #print package information for each row of output based on header information
                print(str(package.truck) + "," + str(packageID) + ", " + str(package.address) + ", " + str(
                    package.city) + ", " + str(
                    package.zipcode) + ", " + str(package.deadline) + ", " + str(package.weight) + ", " + str(
                    package.note) + ", " + str(package.status) + ", " + str(package.deliveryTime) + ", " + str(
                    package.departureTime))
            #print truck mileages - cast the integers to a string so that it concatenates
            print('Total Mileage: ' + str(truck1.distance + truck2.distance + truck3.distance))
        elif (menuOption == "2"):
            #Set up boolean to exit loop when valid packageID is entered
            #break didn't work initially - it only exited the if statement
            switch = True
            while switch:
                packageID = input("Enter package ID: ").strip()
                #make sure the packageID entered is a number
                if packageID.isdigit():
                    #cast the package ID as an integer for logic statement
                    packageID = int(packageID)
                    #check if packageID is within our ID range
                    if 0 < packageID < 41:
                        #turn off the loop
                        switch = False
                    else:
                        print("Package ID not found.")
                else:
                    #If the packageID is not an integer, then redo the loop and prompt the user again.
                    print("Invalid input.")
            #set up another loop to prompt for a valid time input from user
            while True:
                timeInput = input("Enter time in HH:MM:SS format: ")
                try:
                    #parse the string into elements to feed into the datetime object
                    (hrs, min, sec) = timeInput.split(":")
                    timeObj = datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))
                    #if no error occurs - a valid time was entered, exit the loop
                    break
                except ValueError:
                    #if it's an invalid loop - prompt the user to enter the time again
                    print("Invalid input. Please enter time in HH:MM:SS.")
            #grab the package from the hash table based on packageID entered
            package = myHash.search(packageID)
            #if the package entered is 9, check the time input and set the address information based on that
            if packageID == 9:
                if timeObj >= datetime.timedelta(hours=10, minutes=20):
                    package.address = "410 S State St"
                else:
                    package.address = "300 State St"
            #Based on the package's delivery, departure, and time entered, set the package status
            if package.deliveryTime == None and package.departureTime == None:
                package.status = "At hub"
            elif package.deliveryTime == None and package.departureTime > timeObj:
                package.status = "At hub"
            elif package.deliveryTime == None and package.departureTime < timeObj:
                package.status = "En route"
            elif package.deliveryTime > timeObj and package.departureTime <= timeObj:
                package.status = "En route"
            elif package.deliveryTime > timeObj and package.departureTime > timeObj:
                package.status = "At hub"
            else:
                package.status = "Delivered"
            #Print header and package information
            print(
                "Truck ID, PackageID, Address, City, State, Zip, Delivery Deadline, Mass Kg, Notes, Status, Expected Delivery Time, Departure Time")
            print(str(package.truck) + "," + str(packageID) + ", " + str(package.address) + ", " + str(
                package.city) + ", " + str(
                package.zipcode) + ", " + str(package.deadline) + ", " + str(package.weight) + ", " + str(
                package.note) + ", " + str(package.status) + ", " + str(package.deliveryTime) + ", " + str(
                package.departureTime))

        elif (menuOption == "3"):
            # set up a loop to prompt for a valid time input from user
            while True:
                timeInput = input("Enter time in HH:MM:SS format: ")
                try:
                    # parse the string into elements to feed into the datetime object
                    (hrs, min, sec) = timeInput.split(":")
                    timeObj = datetime.timedelta(hours=int(hrs), minutes=int(min), seconds=int(sec))
                    # if no error occurs - a valid time was entered, exit the loop
                    break
                except ValueError:
                    # if it's an invalid loop - prompt the user to enter the time again
                    print("Invalid input. Please enter time in HH:MM:SS.")
            #Print output header
            print(
                "Truck ID, PackageID, Address, City, State, Zip, Delivery Deadline, Mass Kg, Notes, Status, Expected Delivery Time, Departure Time")
            #Loop through all packages within package ID range (1-40)
            for packageID in range(1, 41):
                #Get the package object from the hash table based on package ID
                package = myHash.search(packageID)
                # if the package entered is 9, check the time input and set the address information based on that
                if packageID == 9:
                    if timeObj >= datetime.timedelta(hours=10, minutes=20):
                        package.address = "410 S State St"
                    else:
                        package.address = "300 State St"
                # Based on the package's delivery, departure, and time entered, set the package status
                if package.deliveryTime == None and package.departureTime == None:
                    package.status = "At hub"
                elif package.deliveryTime == None and package.departureTime > timeObj:
                    package.status = "At hub"
                elif package.deliveryTime == None and package.departureTime < timeObj:
                    package.status = "En route"
                elif package.deliveryTime > timeObj and package.departureTime <= timeObj:
                    package.status = "En route"
                elif package.deliveryTime > timeObj and package.departureTime > timeObj:
                    package.status = "At hub"
                else:
                    package.status = "Delivered"
                #print the package information to the console
                print(str(package.truck) + "," + str(packageID) + ", " + str(package.address) + ", " + str(
                    package.city) + ", " + str(
                    package.zipcode) + ", " + str(package.deadline) + ", " + str(package.weight) + ", " + str(
                    package.note) + ", " + str(package.status) + ", " + str(package.deliveryTime) + ", " + str(
                    package.departureTime))
        #Quit program when user enters "4"
        elif (menuOption == "4"):
            break
        #if an invalid menu option is entered, prompt the user again and restart the loop
        else:
            print("Invalid Option. Please Try Again.")

#Initialize the trucks
truck1 = Truck(1)
#Load packages manually on the truck, passing the hash table
#Note: 13, 15, 19 are all on Truck 1 together
truck1.loadPackages([1, 7, 8, 13, 14, 15, 16, 19, 20, 29, 30, 34, 37, 39, 40], myHash)
#set the truck departure time
truck1.departureTime = datetime.timedelta(hours=8)
#deliver the packages
truckDeliverPackages(truck1)
truck2 = Truck(2)
#Note: packages 3, 18, 36, 38 are on Truck 2
#Note: Truck 2 leaves at 9:05am so packages 6, 25 are on truck 2
truck2.loadPackages([3, 4, 5, 6, 10, 11, 18, 21, 22, 23, 24, 25, 26, 31, 36, 38], myHash)
#set the departure time
truck2.departureTime = datetime.timedelta(hours=9, minutes=5)
#deliver the packages
truckDeliverPackages(truck2)
#Load truck 3 with the remaining packages
truck3 = Truck(3)
#Note: package 9 is on truck 3
truck3.loadPackages([2, 9, 12, 17, 27, 28, 32, 33, 35], myHash)
#truck departure time is based on which truck returns first as there's only 2 drivers
#truck 3 will depart at 10:05 am - so the remaining delayed packages will be on truck 3 (28 & 32)
truck3.departureTime = min(truck1.returnTime, truck2.returnTime)
truckDeliverPackages(truck3)

#Call the main menu function for user interface
main()
