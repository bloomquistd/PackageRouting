class Package:
    #Constructor and attributes from the CSV and with default values not provided by the CSV (i.e., deliveryTime)
    def __init__(self, packageID, address, city, zipcode, deadline, weight, note, status):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.note = note
        self.deliveryTime = None
        self.departureTime = None
        self.truck = None
