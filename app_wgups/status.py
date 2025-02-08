#this file creates an enum to standardize the delivery statuses used by the program
from enum import Enum

class PackageStatus(Enum):
    """
    Defines the package status enum for consistent status representation.
    This enumeration ensures that package statuses are used consistently
    throughout the program, preventing errors caused by inconsistent
    string values.

    Attributes:
        AT_HUB (str): Indicates the package is still at the hub.
        EN_ROUTE (str): Indicates the package is currently out for delivery.
        DELIVERED (str): Indicates the package has been successfully delivered.
    """
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"