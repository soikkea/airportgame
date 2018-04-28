# -*- coding: utf-8 -*-

import random

class Flight(object):
    """
    A class representing a single flight
    """
    INCOMING_DISTANCE = 150
    WAITING_DISTANCE = 60

    def __init__(self, name, plane):
        """
        plane must be a Plane object
        """
        self.name = name
        self.plane = plane
        