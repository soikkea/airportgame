"""Description of different planes."""
# -*- coding: utf-8 -*-

class Plane():
    """
    Base class for different plane types.
    """
    def __init__(self, size, max_fuel, max_passengers):
        """
        Constructor
        size = 1...3
        """
        self.size = size
        self.max_fuel = max_fuel
        self.max_passengers = max_passengers
