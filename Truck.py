#Truck constructor with defaults set.
class Truck:
    def __init__(self,ID):
        self.ID = ID
        self.distance = 0.0
        self.currentLocation = "4001 South 700 East"
        self.returnTime = None
        self.departureTime = None
        self.packages = []
    #Function to load the trucks manually based on list.
    def loadPackages(self, packages, myHash):
        self.packages = packages
        #Loop through packages in list and update the package's truck ID once it's loaded.
        for packageID in packages:
            package = myHash.search(packageID)
            package.truck = self.ID

