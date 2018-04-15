# -*- coding: utf-8 -*-

import random
import math

class Airfield(object):
    """
    Airfield that contains runways.
    """
    FIELD_HEIGHT = 200
    FIELD_WIDTH = 400
    RUNWAY_LENGTH_SHORT = 70
    RUNWAY_LENGTH_MED = 100
    RUNWAY_LENGTH_LONG = 150

    def __init__(self):
        self.runway_list = []
        # TODO: airfield size based on difficulty
        self.max_runways = 10
        self.min_runways = 3

        self.create_airfield()
    
    def create_airfield(self):
        """
        Randomly fills the airfield with runways
        """
        number_of_runways = random.randint(self.min_runways,
            self.max_runways)
        
        pass
        # TODO: Finish
