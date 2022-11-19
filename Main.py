import datetime
import re

###################### DEFINE CLASS ######################
# Vehicle Class
class Vehicle:
    def __init__(self, reg, model, price, properties):
        self.reg = reg
        self.model = model
        self.price = price
        self.properties = properties

    def showCar(self):
        print("* Reg. nr: {0}, Model: {1}, Price per day: {2}".format(self.reg, self.model, self.price))
        print("Properties: {0}".format(self.properties))

# Customer Class
class Customer:
    def __init__(self, dateOfBirth, firstName, lastName, email):
        self.dateOfBirth = dateOfBirth
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    
    def writeFile(self):
        return "\n{},{},{},{}".format(self.dateOfBirth, self.firstName, self.lastName, self.email)

# RentedVehicle Class
class RentedVehicles:
    def __init__(self, reg, dateOfBirth,rentedTime):
        self.reg = reg
        self.dateOfBirth = dateOfBirth
        self.rentedTime = rentedTime

###################### FILE HANDLING ######################
# Read file
def ReadFile(nameOfFile, nameOflist):

    file = open("{}.txt".format(nameOfFile), "r", encoding="utf-8")
    content = file.read()
    content = content.strip("\n")
    listOfDetail = list(content.split("\n"))
    file.close()

    for info in listOfDetail:
        if info != []:
            nameOflist.append(info.split(","))

    return nameOflist

# Write file
def WriteFile(nameOfFile, content):

    file = open("{}.txt".format(nameOfFile), "a", encoding="utf-8")
    file.write(content)
    file.close()

# Remove file
def RemoveFile(nameOfFile, reg):
    for i in range(len(listOfDetailRentedVehicles)):
        if(listOfDetailRentedVehicles[i].reg == reg):
            dateOfBirth = listOfDetailRentedVehicles[i].dateOfBirth
            rentedTime = listOfDetailRentedVehicles[i].rentedTime
            break
    try:
        with open("{}.txt".format(nameOfFile), "r") as fr:
            lines = fr.readlines()
            fr.close()
            with open("{}.txt".format(nameOfFile), "w") as fw:
                for line in lines:
                    # strip() is used to remove "\n"
                    # present at the end of each line
                    if line.strip("\n") != "{},{},{}".format(reg, dateOfBirth, rentedTime) and line.strip("\n") != "\n":
                        fw.write(line)
            fw.close()
    except:
        print("Oops! something error") 

###################### DECLARE LISTS ######################
listOfDetailVehicles = []
listOfDetailCustomers = []
listOfDetailRentedVehicles = []

date_format = '%d/%m/%Y'
dateHour_format = '%d/%m/%Y %H:%M'

###################### CONVERT LIST ######################
# Vehicle 
def detailOfVehicles(): 
    listOfVehicles = []
    listOfVehicles = ReadFile("Vehicles", listOfVehicles)
    # Build Object of Vehicle Class
    for i in range(len(listOfVehicles)):
        numberOfArg = len(listOfVehicles[i])
        for j in range(numberOfArg):
            if j == 0:
                reg = listOfVehicles[i][j]
            elif j == 1:
                model = listOfVehicles[i][j]
            elif j == 2:
                price = listOfVehicles[i][j]
            elif j == 3:
                property = listOfVehicles[i][j]
            elif j > 3 and j < numberOfArg:
                property = property + ", " + listOfVehicles[i][j]
        listOfDetailVehicles.append(Vehicle(reg, model, price, property))

# Customer 
def detailOfCustomers():
    listOfCustomers = []
    listOfCustomers = ReadFile("Customers", listOfCustomers)
    for i in range(len(listOfCustomers)):
        numberOfArg = len(listOfCustomers[i])
        for j in range(numberOfArg):
            if j == 0:
                dateOfBirth = listOfCustomers[i][j]
            elif j == 1:
                firstName = listOfCustomers[i][j]
            elif j == 2:
                lastName = listOfCustomers[i][j]
            elif j == 3:
                email = listOfCustomers[i][j]
        listOfDetailCustomers.append(Customer(dateOfBirth, firstName, lastName, email))
    

# Rented Vehicles
def detailOfRentedVehicles():
    listOfRentedVehicles = []
    listOfRentedVehicles = ReadFile("rentedVehicles", listOfRentedVehicles)
    for i in range(len(listOfRentedVehicles)):
        if (listOfRentedVehicles != []):
            numberOfArg = len(listOfRentedVehicles[i])
            for j in range(numberOfArg):
                if j == 0:
                    reg = listOfRentedVehicles[i][j]
                elif j == 1:
                    dateOfBirth = listOfRentedVehicles[i][j]
                elif j == 2:
                    rentedTime = listOfRentedVehicles[i][j]
            listOfDetailRentedVehicles.append(RentedVehicles(reg, dateOfBirth, rentedTime))    
    
###################### CUSTOMER FUNCTIONS ######################
# Check mail format
def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

# Check customer
def checkCustomer(dateOfBirth, reg):

    for i in range(len(listOfDetailCustomers)):
        formatDateOfBirth = datetime.datetime.strptime(listOfDetailCustomers[i].dateOfBirth, date_format)
        if (formatDateOfBirth.year == dateOfBirth.year and formatDateOfBirth.month == dateOfBirth.month and formatDateOfBirth.day == dateOfBirth.day):
            # Old Customer
            firstName = listOfDetailCustomers[i].firstName
            WriteFile("rentedVehicles", "\n{},{},{}".format(reg, dateOfBirth.strftime(date_format), datetime.datetime.now().strftime(dateHour_format)))
            global listOfDetailRentedVehicles
            detailOfRentedVehicles()
            break
        elif i == len(listOfDetailCustomers) - 1:
            # New Customer
            firstName = input("Your first name: ")
            lastName = input("Your last name: ")
            email = input("Your email: ")
            checkMailStatus = checkEmail(email)
            if checkMailStatus:
                newCustomer = Customer(dateOfBirth.strftime(date_format), firstName, lastName, email)
                WriteFile("Customers", newCustomer.writeFile())
                WriteFile("rentedVehicles", "\n{},{},{}".format(reg, dateOfBirth.strftime(date_format), datetime.datetime.now().strftime(dateHour_format)))
                listOfDetailCustomers.append(newCustomer)
                global listOfDetailRentedVehicles
                detailOfRentedVehicles()
                break
            else:
                print("Invalid email. Please try again!")
                return
    print("Hello {}".format(firstName))
    print("You rented the car {}".format(reg))

# Check valid birthday
def checkDateOfBirth(dateOfBirth):
    try:
        dateOfBirth = datetime.datetime.strptime(dateOfBirth, date_format)
        return True
    except ValueError:
        print("Incorrect data format, should be DD-MM-YYYY")

###################### RENTED VEHICLE FUNCTIONS ######################
# Take price of car
def takePriceOfCar(reg):
    for indexCar in range(len(listOfDetailVehicles)):
        if(listOfDetailVehicles[indexCar].reg == reg):
            return round(float(listOfDetailVehicles[indexCar].price), 2)

# Count number of started days
def countNumberOfStartedDays(timeOfPresent, rentedTime):
    return int((timeOfPresent - rentedTime).days)

# -------------- MAIN THREAD --------------------- #
# Define functions of Menu
def listCars():
    print("The following cars are available:")
    for indexCar in range(len(listOfDetailVehicles)):
        for indexRent in range(len(listOfDetailRentedVehicles)):
            if (listOfDetailVehicles[indexCar].reg == listOfDetailRentedVehicles[indexRent].reg):
                break
            elif (indexRent == len(listOfDetailRentedVehicles) - 1):
                listOfDetailVehicles[indexCar].showCar()

def rentCar():
    age = 0
    reg = input("Give the register number of the car you want to rent: ")
    for indexCar in range(len(listOfDetailVehicles)):
        if (listOfDetailVehicles[indexCar].reg == reg):
            dateOfBirth = input("Please enter your birthday in the form DD/MM/YYYY: ")
            timeOfPresent = datetime.datetime.now()
            if checkDateOfBirth(dateOfBirth):
                dateOfBirth = datetime.datetime.strptime(dateOfBirth, date_format)
                age = timeOfPresent.year - dateOfBirth.year - ((dateOfBirth.month, dateOfBirth.day) > (timeOfPresent.month, timeOfPresent.day))
                if (age >= 18 and age < 100):
                    checkCustomer(dateOfBirth, reg)
                    break
                else:
                    print("Your age is not appropriate") 
        elif indexCar == len(listOfDetailVehicles) - 1:
            print("Not found")

def returnCar():
    global listOfDetailRentedVehicles
    reg = input("Give the register number of the car you want to return: \n")
    for indexRent in range(len(listOfDetailRentedVehicles)):
        if (reg == listOfDetailRentedVehicles[indexRent].reg):
            timeOfPresent = datetime.datetime.now()
            rentedTime = datetime.datetime.strptime(listOfDetailRentedVehicles[indexRent].rentedTime, dateHour_format)
            numberOfStartDays = countNumberOfStartedDays(timeOfPresent, rentedTime)
            price = round(takePriceOfCar(reg) * numberOfStartDays, 2)
            dateOfBirth = listOfDetailRentedVehicles[indexRent].dateOfBirth
            status = "\n{},{},{},{},{},{:.2f}".format(reg, dateOfBirth, rentedTime.strftime(dateHour_format), timeOfPresent.strftime(dateHour_format), numberOfStartDays, price)
            print("The rent lasted {} days and the cost is {:.2f} euros".format(numberOfStartDays, price))
            WriteFile("transActions", status)
            RemoveFile("rentedVehicles", reg)
            break
        elif indexRent == len(listOfDetailRentedVehicles) - 1:
            print("The car with this register number is not rented")
    listOfDetailRentedVehicles = []
    detailOfRentedVehicles()

def CountMoney():
    listOfActions = []
    listOfActions = ReadFile("transActions", listOfActions)
    count = 0
    for i in range(len(listOfActions)):
        if (listOfActions[i] != []):
            count = count + float(listOfActions[i][len(listOfActions[i])-1])
    print("The total amount of money is {:.2f} euros".format(count, 2))

# Define Menu function
def Menu():
    detailOfVehicles()
    detailOfRentedVehicles()
    detailOfCustomers()
    while True:
        print("You may select one of the following:")
        print("1) List available cars")
        print("2) Rent a car")
        print("3) Return a car")
        print("4) Count the money")
        print("0) Exit")
        selection = input("What is your selection?\n")
        try:
            if (int(selection) == 1):
                listCars()
            elif (int(selection) == 2):
                rentCar()
            elif (int(selection) == 3):
                returnCar()
            elif (int(selection) == 4):
                CountMoney()
            elif (int(selection) == 0):
                break
            else:
                print("Invalid choice. Enter 0-4")
        except ValueError:
            print("Invalid choice. Enter 0-4")
        
# Menu        
Menu()