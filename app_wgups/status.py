#this file sets up an enum of the 3 statuses
#this ensures the status info is used consistently throughout the entire program

from enum import Enum

class PackageStatus(Enum):
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"